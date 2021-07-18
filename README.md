# Ultimate Tic-Tac-Toe in the terminal

TODO Summary

# How to play
Each small 3 × 3 tic-tac-toe board is referred to as a local board, and the larger 3 × 3 board is referred to as the global board.

The game starts with X playing wherever they want in any of the 81 empty spots. This move "sends" their opponent to its relative location. For example, if X played in the top right square of their local board, then O needs to play next in the local board at the top right of the global board. O can then play in any one of the nine available spots in that local board, each move sending X to a different local board.

If a move is played so that it is to win a local board by the rules of normal tic-tac-toe, then the entire local board is marked as a victory for the player in the global board.

Once a local board is won by a player or it is filled completely, no more moves may be played in that board. If a player is sent to such a board, then that player may play in any other board.

Another version for the game allows players to continue playing in already won boxes if there are still empty spaces. This allows the game to last longer and involves further strategic moves. This is up to the players on which rule to follow. It was shown in 2020 that this set of rules for the game admits a winning strategy for the first player to move, meaning that the first player to move can always win assuming perfect play.

Game play ends when either a player wins the global board or there are no legal moves remaining, in which case the game is a draw.

# How to launch
## Using the Default Pip Setup

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