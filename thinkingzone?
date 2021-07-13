from blessed import Terminal
term = Terminal()
import pygame.time

def thinking_box():
    pygame.time.wait
    print(f"{term.home}{term.white_on_turquoise2}{term.clear}")

    #show t

    #key to exit
    #the window
    y_co = 0
    mul=0
    term.location(x=0, y=0)
    fac = term.width-2
    h = term.height
    if bool(term.height%2):  h = h-1
    s = "PRESS ANY KEY TO EXIT"
    k= "THINKING..."
    t = "time-"
    while(y_co<=h):
     if(y_co==h/2):
        print(f"{term.turquoise2_on_gray1}│"*mul+ f"{term.turquoise2_on_gray1} "*int(fac/6-len(t))+f"{t}"+f"{term.turquoise2_on_gray1} "*int(5*(fac)/6+3)+f"{term.turquoise2_on_gray1}│"*mul, end='\n') 
        print(f"{term.turquoise2_on_gray1}│"*mul+f"{term.turquoise2_on_gray1} "*int((fac+3-len(k))/2)+k+f"{term.turquoise2_on_gray1} "*int((fac+2-len(k))/2)+f"{term.turquoise2_on_gray1}│"*mul,end='\n')
        print(f"{term.turquoise2_on_gray1}│"*mul+f"{term.turquoise2_on_gray1} "*int((fac+3-len(s))/2)+"press any key to exit"+f"{term.turquoise2_on_gray1} "*int((fac+2-len(s))/2)+f"{term.turquoise2_on_gray1}│"*mul,end='\n') 
        y_co = y_co+1       
     elif(y_co>h/2):
        print(f"{term.turquoise2_on_gray1}│"*(mul-1)+f"{term.turquoise2_on_gray1}└"+f"{term.turquoise2_on_gray1}─"*(fac+2)+f"{term.turquoise2_on_gray1}┘"+f"{term.turquoise2_on_gray1}│"*(mul-1),end='\n')
        y_co = y_co+1
        mul = mul-1
        fac = fac + 2
     else:
        print(f"{term.turquoise2_on_gray1}│"*mul+f"{term.turquoise2_on_gray1}┌"+f"{term.turquoise2_on_gray1}─"*fac+f"{term.turquoise2_on_gray1}┐"+f"{term.turquoise2_on_gray1}│"*mul,end='\n')
        y_co = y_co+1
        mul = mul+1
        fac = fac - 2     
    
    term.normal
thinking_box()
