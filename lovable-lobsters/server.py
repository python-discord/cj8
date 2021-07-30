# run this with `uvicorn server:app --reload`

import asyncio
from random import randint
from typing import Literal, TypedDict, Union

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

games: dict[int, tuple[WebSocket, asyncio.Event]] = {}


class ConnectionRequest(TypedDict):
    """Sent when a client wishes to connect to a lobby with code `code`"""

    tag: Literal[1]
    code: int


class GameCreateRequest(TypedDict):
    """Sent when a client wishes to create a lobby. Response is GameMade"""

    tag: Literal[2]


class Ping(TypedDict):
    """Sent when the server wishes to know if a client is still active.

    Client should respond with a Pong, n= the n here.
    """

    tag: Literal[3]
    n: int


class Pong(TypedDict):
    """Sent by the client in response to a Ping"""

    tag: Literal[4]
    n: int


class ErroredRequest(TypedDict):
    """Sent by the server when a ConnectionRequest fails to go through"""

    tag: Literal[5]
    reason: str


class GameMade(TypedDict):
    """Sent by the server in response to a GameCreateRequest"""

    tag: Literal[6]
    code: int


class GoodBye(TypedDict):
    """Sent by the server when the other client has disconnected"""

    tag: Literal[7]


INITIAL_REQUEST = Union[ConnectionRequest, GameCreateRequest]


@app.websocket("/")
async def play_game(websocket: WebSocket) -> None:
    """Creates a link between two websockets, for them to speak to each other."""
    await websocket.accept()
    connect_msg: INITIAL_REQUEST = await websocket.receive_json()

    if connect_msg["tag"] == 1:
        player1, player1_close = games.pop(connect_msg["code"])
    elif connect_msg["tag"] == 2:
        code = randint(10_000, 100_000)
        close_evt = asyncio.Event()
        games[code] = (websocket, close_evt)
        await websocket.send_json({"tag": 6, "code": code})

        # returning closes the connection
        await close_evt.wait()
        return

    try:
        payload: Ping = {"tag": 3, "n": randint(10_000, 100_000)}
        await player1.send_json(payload)
        pong: Pong = await player1.receive_json()

        if pong["tag"] != 4 or pong["n"] != payload["n"]:
            await websocket.send_json({"tag": 5, "reason": "player 1 failed ping"})
    except Exception as e:
        await websocket.send_json({"tag": 5, "reason": str(e)})
        raise  # reraise so normal logic can happen

    # TODO: a better way of doing this? this kinda raises a lot of errors lol
    # at this point we know both p1 and p2 are connected.
    async def worker(first: WebSocket, second: WebSocket) -> None:
        while True:
            msg = await first.receive_text()
            await second.send_text(msg)

    done, _ = await asyncio.wait(
        (worker(player1, websocket), worker(websocket, player1)),
        return_when=asyncio.FIRST_EXCEPTION,
    )

    # one of the websockets disconnected.
    for ws in (player1, websocket):
        try:
            await ws.send_json({"tag": 7})
        except WebSocketDisconnect:
            pass

    # silence annoying asyncio warning
    for task in done:
        try:
            await task
        except WebSocketDisconnect:
            pass

    player1_close.set()
