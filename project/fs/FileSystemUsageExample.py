from Dir import Dir
fs = Dir.FromPath("../OS", None, 7, 0, 0)


class User:
    "temporary user class"
    uid = 0


thisDir = fs
while True:
    command = input("your command: ")
    if command == "ls":
        for i in thisDir.ls(User).keys():
            print(i)
    elif command[:2] == "cd":
        try:
            thisDir = thisDir.getDir(User(), command[3:])
        except Exception as e:
            print(e)
    elif command[:5] == "mkdir":
        try:
            thisDir.mkdir(User, command[6:])
        except Exception as e:
            print(e)
    elif command[:5] == "touch":
        try:
            thisDir.touch(User, command[6:])
        except Exception as e:
            print(e)
    elif command[:2] == "rm":
        try:
            thisDir.rm(User, command[3:])
        except Exception as e:
            print(e)
