from os import sep
from os.path import abspath, dirname
import string

# sep is separator in Host OS

# Create our table of all characters.
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

# Home prefab path
etcskel = "/etc/skel"

# Template for down and up when printing boxes
template = '{0}{1}/{2}/{3}{4}'

# main path
MAIN_PATH = dirname(abspath(__file__)) + sep + ".." + sep

# Start Path
START_PATH = MAIN_PATH + "OS"

# Blank Lines
BLANK_LINES = 50

# Loading bar
LOADING_BAR = "."
