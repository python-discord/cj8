cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]

def virtualmachine(res):
    retstring = ""
    res1, res2 = res.split("x")
    res1 = int(res1)
    res2 = int(res2)
    retstring += str(cl[2] + cl[1]*int(int(res1)-2) + cl[4] + "\n")
    for _ in range(res2):
        retstring += str(cl[0] + " "*int(res1 - 2) + cl[0] + "\n")
    retstring += str(cl[8] + cl[1]*int(int(res1)-14) + cl[4] + "  " + cl[2] +cl[10] + "\n")
    retstring += str(" "*int(int(res1)-6) + cl[8] + cl[0]*2 + cl[10] + "  ")
    return(retstring)
    
print(virtualmachine("10x10"))  