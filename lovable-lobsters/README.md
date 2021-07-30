# Ultimate Tic-Tac-Toe in the terminal

<img src="https://upload.wikimedia.org/wikipedia/commons/d/d1/Incomplete_Ultimate_Tic-Tac-Toe_Board.png" alt="drawing" width="200"/>

Thinking inside a box, that is inside a box, that is inside yet another box.

# Table of contents
This document will contain the following information:
1. [How to play](#how-to-play)
2. [How do I launch it?](#how-do-i-launch-it)
    1. [Building the environment](#building-the-environment)
    2. [Starting the Game](#starting-the-game)
3. [Terminology](#terminology)

# How to play
- `The Board` Each small 3 × 3 tic-tac-toe board is referred to as a Sub-Grid, and the larger 3 × 3 board is referred to as the global board.

- `Game Start` The game starts with player X placing a token wherever they want.

- `Taking a Turn` This move will "send" their opponent to the sub-grid based on the space in the sub-grid player X placed their token. For example, if X placed their token in the top right square in the bottom left sub-grid, then player O needs to play next in the sub-grid at the top right of the global board. Player O can then play in any one of the nine available spots in that sub-grid.

- `Winning a Sub-Grid` If a move is played so that it is to win a sub-grid by the rules of normal tic-tac-toe, then the entire sub-grid is marked as a victory for the player in the global board.

- `Wildcard Selection` Once a sub-grid is won by a player or it is filled completely, no more moves may be played in that board. If a player is sent to such a board, then that player may play in any other board.

- `Victory Conditions` Game play ends when either a player wins the global board or there are no legal moves remaining.

# How do I launch it
## Building the environment
### Using the Default Pip Setup
Our default setup includes a bare requirement file to be used with a [virtual environment](https://docs.python.org/3/library/venv.html).

We recommend this if you never have used any other dependency manager, although if you have, feel free to switch to it. More on that below.

### Creating the environment (not necessary but recommended)
Create a virtual environment in the folder `.venv`.
```shell
$ python -m venv .venv
```

### Enter the environment
It will change based on your operating system and shell.
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

### Installing the Dependencies
Once the environment is created and activated, use this command to install the development dependencies.
```shell
$ pip install -r requirements.txt
```

If you wish to play via the network. Run the following
```shell
$ pip install -r server-requirements.txt
```

### Exiting the environment
Interestingly enough, it is the same for every platform
```shell
$ deactivate
```
## Starting the Game

### Single Terminal
Be in the root directory
From your terminal enter the following commands:
```shell
$ python main.py
```

### Two Terminals
Be in the root directory
From two terminals enter the following commands:
```shell
$ python main.py
```
From a third terminal enter the following command:
```shell
$ uvicorn server:app
```

From terminal 1 be sure to select 'y' to the following prompt:
<img src="https://raw.githubusercontent.com/A5rocks/code-jam-8/main/docs/wired_prompt.PNG" alt="drawing" width="300"/>

When asked for the websocket be sure to type in the IP address and port number of the machine running the webserver. 

<img src="https://raw.githubusercontent.com/A5rocks/code-jam-8/main/docs/websocket_entry.PNG" alt="drawing" width="300"/>

After which be sure to create a lobby when asked. This will give you a lobby code. Follow a similar procedure as above on the second terminal but when it prompts the user if they want to create a lobby say no. It will then ask the user the lobby code of terminal 1. 
<img src="https://raw.githubusercontent.com/A5rocks/code-jam-8/main/docs/lobby_code.PNG" alt="drawing" width="600"/>

# Terminology
<img src="https://github.com/A5rocks/code-jam-8/blob/main/docs/terminology.png?raw=true" alt="drawing" width="600"/>