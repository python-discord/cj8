![Panthera's Box Logo][logo]

[logo]: img/PantherasBox.png "Panthera's Box"

Panthera's Box is a terminal-based game about putting everything that has escaped the box back in.

> All of life’s miseries had been let out into the world.
> She slammed the lid of the box back down. The last thing remaining inside of the box was hope.
> Ever since, humans have been able to hold onto this hope in order to survive the wickedness that she had let out.

## Installation & Running

Panthera's Box can be installed and run using two different methods:

### Installing as a package

1. Install with `pip`:

    1.1a `pip install .` (Local)

    or

    1.1b `pip install git+https://github.com/Willd14469/cj8-patient-panthers` (Git)

    This will install the game as the package `pantheras_box`.

2. Run the game: `pantheras-box`

### Running without installing as a package

1. Install dependencies: `pip install -r dev-requirements_[win|unix].txt`

2. Run the game: `python main.py`

### Arguments

`--flush-log` - truncate the log file

`--flush-score` - delete the high-scores file

### Notes

Turn down the channel that is running the terminal, as the game sounds can be fairly loud.

The terminal should be at least 75x40, in order to render the board correctly.

## Game Guide

The game consists of a ball and sets of redirector arrows. To complete each level, guide the ball towards the goal, by rotating the arrows. Hidden story tiles are scattered throughout the maps, requiring the player to take different paths.

On each level, a random set of mutators will be activated, modifying the gameplay slightly; this includes inverted controls, limited field of view and increased speed.

Scores are determined by the number of moves and time taken during a level. The maximum score attainable is relative to the board size. If a player's score reaches zero, the game is over.

## Levels

Levels are stored in `pantheras_box/backend/levels/`.

In short, levels are images that define the layout of the initial board. After parsing colour and co-ordinates, they are translated into a two-dimensional list of tiles.

## Libraries

- [rich](https://pypi.org/project/rich/) - front-end graphical library
- [Pillow](https://pypi.org/project/Pillow/) - parse level images
- [boombox](https://pypi.org/project/boombox/) - cross-platform audio player
- [PyYAML](https://pypi.org/project/PyYAML/) - configuration file format
- [keyboard](https://pypi.org/project/keyboard/) - keyboard handler (Windows)
- [pynput](https://pypi.org/project/pynput/) - keyboard handler (Unix)

## Platform Compatibility

The game works and has been tested on both **Windows** and **Linux (Arch & Debian)**.

In theory, the game should work on **MacOS**, but this has not been tested.

For best results:
   - Use **Powershell** within **Windows Terminal** on Windows
