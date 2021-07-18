# Welcome To Robust Reindeer! #

This submission to the 8th Code-Jam of the Python-Discord channel is a
Rubik's cube, rendered in a text user interface (that was a
constraint) using the asciimatics package, and addressing the theme
"thinking inside the box".

Just like a real world Rubik's cube, you can move this cube around to
look at it from all sides. And, of course, you can rotate the
individual discs it is made up of to first scramble up the order and
then to try and solve it into perfect ordering again.

For more info, please select either "Mouse Movements" or "Keyboard
Commands" buttons from above, and they will help you to see how to use
our Rubik's Cube!

## INSTALLATION

This app has been written for Python 3.9.4, but other versions of
Python 3.9 should work, too. So make sure you are using one of those.

Clone this repository

``` bash
    git clone https://github.com/bjoseru/pdcj8-robust-reindeer.git
```

then change into the cloned directory, create a virtual environment to
separate this from your usual Python environment, and activate it

``` bash
    cd pdcj8-robust-reindeer
    python -m venv .venv
    . .venv/bin/activate
```

Now install the dependencies
``` bash
    pip install -r dev-requirements.txt
```

You are now ready to run the app with
``` bash
    python ./cube.py
```

## COMMANDS##

For the following, lowercase means "counter-clockwise" or
"anticlockwise", and uppercase means clockwise.

- Rotate Front: f/F

    Press f or F to rotate the front disc.

- Rotate Middle: m/M

    Press m or M to rotate the middle disc.

- Rotate Back: b/B

    Press b or B to rotate the back disc.

- Rotate Top: t/T

    Press t or T to rotate the top disc.

- Rotate Bottom: d/D

    Press d or D to rotate the bottom disc.

- Rotate Left: l/L

    Press l or L to rotate the left disc.

- Rotate Right: r/R

    Press r or R to rotate the right disc.

### Other Commands ###

- Reset View: z

    Press r to return to the starting view

- Help: h

    Shows this menu

- Quit: q/Q/Ctr+q/Ctr+x

    Press q, Q, Ctr+Q or Ctr+X to exit the cube.

### Mouse Movements ###

- Mouse Click:

    Click the mouse to toggle free rotation of the cube with the
    mouse. This only applies if your terminal supports it.

- Mouse Drag / Move:

    Rotate the cube.

## AUTHORS AND LICENCE ##

This project has been designed and coded in about a week by the
following Robust Reindeer team, consisting of the Python-Discord
members:

- Björn (team-lead)
- aaronshenhao
- mathsman
- Dude Saber
- HellRevenger
- Keppo

Contributions included conception, the mathematics required for the
geometry and 3D rendering, exploration of TUI frameworks, various
proof-of-concept prototypes, the final coding, and of course this
documentation.

This code is licenced unter [The MIT License](https://opensource.org/licenses/MIT).

## OUTLOOK ##

While the project is presentable, some additional improvements could
still be made. Since this project is licensed under the MIT licence,
you are more than welcome to add to it. The following would be nice to
have:

- Improvements to the frame rate in high-resolution terminals, perhaps
  by not clearing the entire terminal in each frame.
- Animation of the disc rotations.
- A "scramble the cube" option.
- A "show me the solution from here" option.
