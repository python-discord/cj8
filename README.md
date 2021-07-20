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

The game consists of a ball and sets of redirector arrows. To complete each level, guide the ball towards the goal, by
rotating the arrows. Hidden story tiles are scattered throughout the maps, requiring the player to take different paths.

On each level, a random set of mutators will be activated, modifying the gameplay slightly; this includes inverted
controls, limited field of view and increased speed.

Scores are determined by the number of moves and time taken during a level. The maximum score attainable is relative to
the board size. If a player's score reaches zero, the game is over.

## Levels

Levels are stored in `pantheras_box/backend/levels/`.

In short, levels are images that define the layout of the initial board. After parsing colour and co-ordinates, they are
translated into a two-dimensional list of tiles.

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

## Architecture

Panthera's Box has 5 main modules:

- `backend` - state of the game
- `frontend` - displaying the game
- `keyboard_handlers` - receiving input from the user
- `sounds` - playing sounds
- `story` - loading and displaying the correct story for the game state

Each of these modules are responsible for a cornerstone of the application. Communication between these modules is
handled by an event system (`backend.events`) that allows modules to add a callback to hook into events that have been emitted.
This allows each module to be independent and not need context of other modules. The backend module emits events such as
`ball_movement` and `level_loaded` to broadcast the fact that the game state has changed fundamentally.

The frontend module is responsible for the render loop as well as prompting the backend to advance the game a single
tick.
Mutators (`backend.mutators`) are responsible for changing the parameters of the backend module to alter gameplay.
These effects increase the variety of gameplay.

#### Key input

Keyboard input has its own module, due to having multiple packages for handling the input. A factory pattern is used to
determine which type of keyboard handler to use. `keyboard` is used on _Windows_, as it provides a very clean way to
handle inputs. However, on _Unix_, root is required to access input devices (`uinput` kernel module), so `pynput` is used
instead for its `xorg` backend.

#### Logging

Panthera's Box logs all the events that get emitted, if logging is set to `DEBUG`, to get full visibility of the communication
between the core components. If logging is set higher than `DEBUG`, then the events will only write warnings to the logger to
save on performance.

#### Config

`pantheras_box/config.py` provides a simple way to alter file location of score and log files. It also allows for modifying the logging
level.

## Roadmap

- Implement all the core modules as singletons
   - They can be referenced without having to implicitly pass them as arguments
   - Ensures only one instance of each module exists
- Improve render loop so only updated elements are re-rendered to decrease load
- Add trap tiles
- Mutators with positive effect
