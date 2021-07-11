
def prinstart(arg):
    print(term.clear)
    print(term.green_on_black(arg))
    time.sleep(3)
    print(term.green_on_black("Press C to continue"))
    with term.cbreak():
        val = ''
        if val.lower() == 'q':
            return
        else:
            continue

if __name__ == "__main__":
    printstart("""Hey There! \n  You are an Artificial Intelligant, built by the USA, developed to get into PCs and analyze them. \n You was hacked into a System by the Atomic Program of the Iran. Here, ur job was to analyze the Data and to see if there are any files which could gives hint to the Atomatic Missiles of the Iran. \n \n""")
    printstart("""You found out that there will be a Atomatic launch today, it should hit the US. But unfortunally, the system is offline, you cant contact the USA to warn them. \n \n""")
    printstart("""Because of that, u decide that ull try to turn of the System, because you found indicates that that will stop the attack. But unfortunally, you need Root Privilages to shutdown the Operating System \n \n""")
    printstart("""You can gain access to these by (*insert challange here, example: get thr password of the main file*). You will have to overcome multiple challenges \n \n""")
    vrintstart("""So, dont waste your time, think smarter not harder, and good luck!
(*Title* starting, 
gaining system access,
Access gained.
AI will launch...) \n \n""")
    
