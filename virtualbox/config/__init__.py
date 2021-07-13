from os import sep
from os.path import abspath, dirname
import string

# sep is separator in Host OS

# Create our table of all characters.
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

# Home prefab path
etcskel = "/etc/skel"

# Start Path
START_PATH = dirname(abspath(__file__)) + sep + ".." + sep + "OS"

# Blank Lines
BLANK_LINES = 20

# # Loading bar
# Loading_bar = "////////////"
