# Acute Aligators 2021 Python Discord Summer Code Jam

## Setup (tested on linux):
Set up virtual enviroment: <br>
`python3.9 -m venv venv` <br>
Install requirements: <br>
`pip install -r requirements.txt` <br>
Start virtual environment: <br>
source venv/bin/activate

## Running game:
There are two commands to run the game. The most basic one is: <br>
`python app.py` <br>
When running on linux sometimes the screen will bounce up and down. To avoid this you can try: <br>
`python app.py --bless`

## Dungeons and Dragons game play: <br>
This is a rogue like game where the dungeon is built on your file directory. Each sub-directory is another room in the dungeon. The goal is to make it to the deepest depth of your file structure.


Use wasd to control your character. There are monsters that will try to kill you along the way. Combat is based on a rock, paper, scissors color system. Red beats green, green beats blue, and blue beats red. You can walk over the colored @ signs to change the color of your character. Monsters will behave differently depending on your color.
