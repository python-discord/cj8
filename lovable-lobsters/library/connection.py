import enum
import json
import queue
import threading
import typing

# (no type stubs :( )
import websocket  # type: ignore [import]


class Tags(enum.IntEnum):
    """Tags for tagged tuples (no ADTs :( )"""

    GAME_MADE = 1
    GAME_STARTED = 2
    PLACE_SQUARE = 3
    DISCONNECTED = 4


TAGGED_TUPLES = typing.Union[
    # game was made, second is game code.
    tuple[typing.Literal[Tags.GAME_MADE], int],
    # game can start, other player joined.
    tuple[typing.Literal[Tags.GAME_STARTED]],
    # move to `subgrid`, `square`.
    tuple[typing.Literal[Tags.PLACE_SQUARE], int, int],
    # disconnected
    tuple[typing.Literal[Tags.DISCONNECTED]],
]

QUEUE = queue.Queue[TAGGED_TUPLES]


def _establish_connection(
    inputs: QUEUE, outputs: QUEUE, code: typing.Optional[int], url: str
) -> None:
    ws = websocket.create_connection(url)

    if not code:
        # make the lobby
        ws.send(json.dumps({"tag": 2}))
        resp = json.loads(ws.recv())

        if resp["tag"] != 6:
            return

        game_code = resp["code"]

        outputs.put((Tags.GAME_MADE, game_code))

        # wait until another player joins
        ping = json.loads(ws.recv())

        if ping["tag"] != 3:
            return

        ws.send(json.dumps({"tag": 4, "n": ping["n"]}))
    else:
        # join the lobby
        ws.send(json.dumps({"tag": 1, "code": code}))

    # now we have a direct connection to the other player
    # for some reason, mypy thinks this is `outputs.put(tuple[Tags])`?
    outputs.put((Tags.GAME_STARTED,))  # type: ignore [arg-type]

    # now, if a player disconnects, the other session will notice when it's not their turn but like...
    # whatever.

    # player who made the lobby goes first
    if not code:
        input_msg = inputs.get()
        if input_msg[0] != Tags.PLACE_SQUARE:
            return

        tag, subgrid, square = input_msg

        ws.send(json.dumps({"tag": 8, "subgrid": subgrid, "square": square}))

    while True:
        msg = json.loads(ws.recv())
        if msg["tag"] == 7:
            # for some reason, mypy thinks this is `outputs.put(tuple[Tags])`?
            outputs.put((Tags.DISCONNECTED,))  # type: ignore [arg-type]
            return
        elif msg["tag"] != 8:
            return
        outputs.put((Tags.PLACE_SQUARE, msg["subgrid"], msg["square"]))

        input_msg = inputs.get()
        if input_msg[0] != Tags.PLACE_SQUARE:
            return

        tag, subgrid, square = input_msg

        ws.send(json.dumps({"tag": 8, "subgrid": subgrid, "square": square}))


def create_connection(code: typing.Optional[int], url: str) -> tuple[QUEUE, QUEUE]:
    """Create a connection to the multiplayer server

    Returns a tuple of (inputs, outputs)

    inputs is a queue that is `.put` to place a space, and outputs is a queue
    that is `.get` to get connection info and to find when opponent placed a
    space.
    """
    inputs: QUEUE = queue.Queue[TAGGED_TUPLES]()
    outputs: QUEUE = queue.Queue[TAGGED_TUPLES]()
    threading.Thread(
        target=_establish_connection, args=(inputs, outputs, code, url)
    ).start()

    return inputs, outputs
