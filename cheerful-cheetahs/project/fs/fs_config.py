from sys import platform
import string

"Create our table of all characters."
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

"Separator in host OS"
sep = "\\" if platform == "win32" else "/"
