# Acute Aligators 2021 Python Discord Summer Code Jam

![Acute Aligators](/alligators1.png)

## Demo
https://youtu.be/nFNKscvKVQY

## Setup (tested on linux):
Set up virtual enviroment: <br>
`python3.9 -m venv venv` <br>
Install requirements: <br>
`pip install -r requirements.txt` <br>
Start virtual environment: <br>
`source venv/bin/activate`

## Setup (tested on windows):
Set up virtual enviroment: <br>
`python3.9 -m venv venv` <br>
Install requirements: <br>
`pip install -r requirements.txt` <br>
Start virtual environment: <br>
<br>
if running from the command line: <br>
activate the venv with ``venv/scripts/activate.bat``

if running from powershell:<br>
activate the venv with ``venv/scripts/activate.ps1``

## Running game:
The most basic run command is: <br>
`python app.py` <br>
When running on linux sometimes the screen will bounce up and down. To avoid this you can try: <br>
`python app.py --bless` <br>
Playing in a different directory <br>
`python app.py --path /home` <br>
Or using a relative path <br>
`python app.py --path ../..`

![Dungeons and Directories](/dugeons-and-directories.png)

## Dungeons and Directories game play: <br>
This is a rogue like game where the dungeon is built on your file directory. Each sub-directory is another room in the dungeon. The goal is to make it to the deepest depth of your file structure.


Use wasd to control your character. There are monsters that will try to kill you along the way. Combat is based on a rock, paper, scissors color system. Red beats green, green beats blue, and blue beats red. You can walk over the colored @ signs to change the color of your character. Monsters will behave differently depending on your color.

`#` are doors that will bring you to the next directory.

## Framework and theme
The TUI we used is Rich. We took advantage of its panels and colors among other features. The project is connected to the theme "Think inside the box" in several ways. Directories are a sort of box that hold folders and files. When playing without the path flag the dungeon of the game will be the same files and folders that make up the project. Finally, this game is inspired by rogue-likes, which is an in the box idea that has done many times before.
