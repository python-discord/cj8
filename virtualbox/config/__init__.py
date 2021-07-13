from os import sep
from os.path import abspath, dirname
import string


"Create our table of all characters."
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

"Separator in host OS"
sep = "\\" if platform == "win32" else "/"

"Home prefab path"
etcskel = "/etc/skel"

