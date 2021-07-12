from random import randint

# portscanner function for command usage
def portscanner(user_input, fs, user):
    try:
        # if user_input contains specific port specifies var
        if user_input[1]:
            use_true = 'temp'
    except:
        pass
    ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    outputs = ['not a hint', 'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    # if specified var (= if user_input contains specific port)
    if use_true:
        # Different Prints to show user a portscanner experience and show hint/ no hint
        print(term.green_on_black(f'Scanning Network for Port: {user_input}'))
        time.sleep(1)
        clear_term()
        print(term.green_on_black(f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n"))
        time.sleep(1)
        clear_term()
        output = random.choice(outputs)
        clear_term()
        print(term.green_on_black(f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n'))
    else:
        # 5-7 to show user a portscanner experience and show hint/ no hint
        for i in range(randint(5, 7)):
            port = ports[i]
            print(term.green_on_black(f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n"))  # term.green_on_black
            time.sleep(0.4)
        inp = input(term.green_on_black('Select a port to scan: '))
        inp = int(inp)
        with term.cbreak():
            val = ''
            if int(val.lower()) in ports:
                output = random.choice(outputs)
                time.sleep(3)
                clear_term()
                print(term.green_on_black(f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n'))

            else:
                print(term.green_on_black('The Port you entered wasnt found in the Network!'))
