
def prinstart(arg):
    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.green_on_black(arg))
    time.sleep(3)
    print(term.green_on_black("Press C to continue"))
    with term.cbreak():
        val = ''
        if val.lower() == 'c' or val.lower() == 'C':
            time.sleep(1)
            return
        else:
            pass

def gameloads(arg):
    print(term.green_on_black(arg))
    time.sleep(2)
    return

if __name__ == "__main__":
    printstart("""Hey There! \n  You are an Artificial Intelligant, built by the USA, developed to get into PCs and analyze them. \n You was hacked into a System by the Atomic Program of the Iran. Here, ur job was to analyze the Data and to see if there are any files which could gives hint to the Atomatic Missiles of the Iran. \n \n""")
    printstart("""You found out that there will be a Atomatic launch today, it should hit the US. But unfortunally, the Computer is offline, you cant contact the USA to warn them. \n \n""")
    printstart("""Because of that, you decide that you'll try to turn of the System, because you found indicates that that will stop the attack. But unfortunally, you need Root Privilages to shutdown the Operating System \n \n""")
    printstart("""You can gain access to these by (*insert challange here, example: get the password of the main file*). You will have to overcome multiple challenges \n \n""")
    printstart("""So, dont waste your time, think smarter not harder, and good luck!""")
    gameloads("*Title* Starting,")
    gameloads("Gaining System Access,")
    for _ in range(10):
       print(term.green_on_black("-"*_ + "_"*int(_ - 10) + "  " + str(_*10) + "%"))
       time.sleep(0.2)
    gameloads("Access Gained,")
    gameloads("AI launched successfully,")
    
