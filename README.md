# Are You in a Box?

You're confined in what seems like gigantic, labyrinthine boxes, and you have to escape. However, the only way to get out of each box is to tag its four outer walls... and deception can be around every corner. Can you successfully complete the 7 levels?

Use arrow keys or WASD to move around, and whenever you're sure that you've found an outer wall of the box, use Shift + WASD to tag the upper, left, lower, and right walls respectively. Instructions are also in the game.

Sound effects credits at [`sfxcredits.md`](https://github.com/mirandazellnik/code-jam-2021/blob/main/sfxcredits.md).

-------------------
## Demo Video
A demonstration with explanation of basic mechanics can be seen below.

[![fig1](https://i.ytimg.com/vi/mx8o-1wJdzc/hqdefault.jpg)](https://www.youtube.com/watch?v=mx8o-1wJdzc)



## Installation

### Extra steps for Linux users
Linux users need to install the external *PyGObject* library before doing the installation steps bellow ([installation instructions here](https://pygobject.readthedocs.io/en/latest/getting_started.html)). Then, *Pycairo* and *PyGObject* for python need to be installed as well.

```
python -m pip install pycairo PyGObject
```

In case of errors, a `no-sound` fallback branch is available.


### Installation Steps
1. Download [the VCS *Git*](https://git-scm.com/downloads). In your terminal, change to your desired directory that the code will be in (`cd` command), and run `git clone https://github.com/mirandazellnik/code-jam-2021`.
2. `cd` into the code jam folder (by default its name is `code-jam-2021`), and open up a virtual environment with the `python -m venv .venv` command.
3. Activate the venv. This will depend on your OS and terminal, so here's a list of commands below.  
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
4. Install the dependencies by running `pip install -r dev-requirements.txt`. This might take a while.
5. Finally, run `python main.py` to start the program. Enjoy!

-----------------
## OS/Terminal-specific Incompatibilities & Extra Dependencies
Below is a list of incompatibilities discovered so far that depends on your operating system/terminal.

* Windows - Windows Shell, PowerShell, `cmd.exe`: `asciimatics` won't give support for the 256 color-palette, and so a fallback is used with only black and white (no gray-gradient lighting D:).
