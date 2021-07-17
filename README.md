# Are You in a Box?
You're confined in what seems like gigantic, labyrinthine boxes, and you have to escape. However, the only way to get out of each box is to tag its four outer walls... and deception can be around every corner. Can you successfully complete the 7 levels?

Instructions are in the game. Sound effects credits at [`sfxcredits.md`](https://github.com/mirandazellnik/code-jam-2021/blob/main/sfxcredits.md).

## OS/Terminal-specific Incompatibilities & Extra Dependencies
Below is a list of incompatibilities discovered so far that depends on your operating system/terminal.

* Windows - Windows Shell, PowerShell, `cmd.exe`: `asciimatics` won't give support for the 256 color-palette, and so a fallback is used with only black and white (no gray-gradient lighting D:).
* Linux - `playsound` seems to bug out on Linux, where you'll have to manually install the `gi` module. It could also just not work at all, in which case, check out our sound-less fallback branch.
