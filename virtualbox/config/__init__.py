<<<<<<< HEAD
from os import sep
from os.path import abspath, dirname
=======
from sys import platform
>>>>>>> parent of 67bb69f (new argument system, unicode in spearate file and in config)
import string

# Create our table of all characters.
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

# Separator in host OS
sep = "\\" if platform == "win32" else "/"

# Home prefab path
etcskel = "/etc/skel"

# Template for down and up when printing boxes
template = '{0}─/{1}/{2}{3}'

# Start Path
START_PATH = "OS"

# Blank Lines
BLANK_LINES = 50
