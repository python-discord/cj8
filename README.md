![Panthera's Box Logo][logo]

[logo]: img/PantherasBox.png "Panthera's Box"

Panthera's Box is a terminal-based game about putting everything that has escaped the box back in.

## Installation & Running

Panthera's box can be installed and run using two different methods:

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

`--flush-log` - Will truncate the log file

`--flush-score` - Will delete the high-scores file

### Notes

Turn down the channel that is running the terminal as the game sounds can be fairly loud.

## Game Guide

The game consists of a ball and sets of redirector arrows. To complete each level, guide the ball towards the goal, by rotating the arrows. Hidden story tiles are scattered throughout the maps, requiring you to take different paths.

## Platform Compatibility

The game works and has been tested on both **Windows** and **Linux (Arch)**

In theory the game should work on **MacOS** but this has not been tested.

For best results: 
   - Use **Powershell** within **Windows Terminal** on Windows
