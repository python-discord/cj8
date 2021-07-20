# Jubilant Jellyfish Platformer Game

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Challenges we faced](#challenges-we-faced)
4. [Files](#files)
5. [Problems](#problems)

## Introduction

Hello, there! Welcome to the GitHub repository of the Jubilant Jellyfish project to Python Discord's Summer Code Jam in 2021. 

The project is a platform game that can be played in the terminal, where you must move a jellyfish in the map to push some boxes into their places. Your time is limited though! You can see how much time is left to complete the level on the top-mid of the screen. If you need time to think about how you can solve the current level, just enter the grey thinking box, and the timer will stop. Keep in mind, that jellyfishes need a calm place to think, so there is dark and quiet inside the box: You cannot see the level when you're inside.

You might be thinking about why we chose to create such a project, so let me explain. The technology of this code jam was Terminal User Interfaces (TUIs), so it was given that we should create something that runs in the terminal. The theme of the jam was 'Think inside the box', and our team had the name 'Jubilant Jellyfish'. After all this was announced, we sat down to brainstorm ideas about what would be a fun way to implement these constraints. It actually didn't take long to settle on the idea of a game, and soon after we connected all the dots and the goal was very visible. We then had 1 week to achieve what we wanted.

OK, Daniel, good story, but now I want to play. How can I do that?
After running through the [installation](#installation), you can just run `main.py` in your terminal.

## Installation

1. Installing XTerm for resizing the terminal window:
    - Ubuntu, Kali, Debian:
        > `sudo apt-get install xterm`
    - Arch:
        > `pacman -Syu xterm`
    - MacOS:
        > `brew install xterm`
    - Windows:
        > We could not find a way to easily resize the terminal, but the other parts of the project run relatively well in PowerShell.

2. Installing dependencies:
    - `pip install -r requirements.txt` with the `requirements.txt` of this repository
    > Note: Use a virtual environment

## Files

Here is a list of the relevant files of the project, and what they contain:
- `LICENSE`: [The MIT License](https://opensource.org/licenses/MIT), an OSS approved license which grants rights to everyone to use and modify this project.
- `requirements.txt`: Every PyPI packages used for the project's development.
- `main.py`: This script controlls the gameloop and all the parts that interact with the user. It's the heart of the game. (teamwork)
- `maps.py`: Contains a class that has methods for building the levels, binding graphics and physics together. (teamwork)
- `sprites.py`: Contains classes for building and drawing the different graphical objects. (Mihaela's work)
- `physics2.py`: Provides a `Space` class and an Object class for handling collisions, applying gravity, and getting position-based events. (Daniel's work)

## Challenges we faced

We had to face some serious challenges during this competition that I wanted to say a few words about:
1. **Crew Problem**

    By the 3rd day of the coding part, just 2 of us have remained active, neither of us having more than a year of coding experience. So please don't view this project as a very serious work done by experts. We just wanted to gain experience and have fun.
    
2. **Low resolution display**

    TUIs by their nature are not meant to display games with moving elements, and this shows in some aspects of the project. For example, the technology I based my physics engine on (pygame.Rect) uses only ints, and we used graphical elements that were less than 5 pixels high or wide, with the platform elements being only 1 pixel high. To this problem I came up with the solution of upscaling the whole physical simulation of the action, so that we can use bigger ints for accuracy, and then reducing the coordinates before rendering.
    
3. **Flickering and building from chars**

    I asked Mihaela, what were some of the challenges she had to face.
    
    *For me, the hardest part was dealing with a constantly blinking screen. It took pretty much time figuring out what was causing it, but it turned out it was the framework's problem so we left it this way. Another time consuming task I faced was building the objects from characters. It took some time and it was boring to copy paste the same command over and over, but I am happy on how the sprites turned out in the end.* - Mihaela

## Problems

### You cannot pass Level 2

```
        target1 = Target(0, 24, self.terminal)
        self.space.add_object(70, 21, TARGET_W, TARGET_H, type="target")
```

These are the lines 111-112 from `maps.py`. Why does this matter? `Target` and `Space.add_object` both accept `left` and `top` as their first arguments, and because of this, target1 is not displayed where it actually is. This error only got noticed hours after submission, so we couldn't fix it. It will be changed as soon as the jam is closed, or you can change the code to place them both at (0, 24).

### Flickering

The game is still flickering hard. We couldn't find a solution to that yet. Don't hesitate to alert us if you know something that might fix it.

### Style

We had no time left in the end to document our code and make it comply with `flake8`. This will soon be fixed after the closing of the Code Jam.

## Contact Us

Should you have any questions or recommendations, feel free to contact us at:
- Daniel Buza (@danib-prog) - [9buza.dani@gmail.com](9buza.dani@gmail.com)
- Mihaela Grajdan - [mihaelagrajdan3102003@gmail.com]

