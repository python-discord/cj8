from sys import platform
import string
import os

# Create our table of all characters.
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

# Separator in host OS
sep = "\\" if platform == "win32" else "/"

# Home prefab path
etcskel = "/etc/skel"

# Template for down and up when printing boxes
template = '{0}─/{1}/{2}{3}'

# Start Path
START_PATH = os.path.dirname(os.path.abspath(__file__)) + sep + ".." + sep + "OS"

# Blank Lines
BLANK_LINES = 50
