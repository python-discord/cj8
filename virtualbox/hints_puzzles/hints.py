def portscanner(user_input, fs, user):
    try:
        if user_input[1]:
            use_true = 'temp'
    except:
        pass
    "portscan - commits portscan"
    ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    outputs = ['not a hint', 'not a hint', 'not a hint', 'not a hint', 'not a hint', 'a hint', 'a hint', 'a hint', 'a hint']
    if use_true:
        print(f'Scanning Network for Port: {user_input}')
        time.sleep(1)
        clear_term()
        print(f'f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n"')
        time.sleep(1)
        clear_term()
        output = random.choice(outputs)
        clear_term()
        print(f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n')
    else:
        for i in range(7):
            port = ports[i]
            print(
                str(f"Found Port in Network: \n    {port}/TCP [State: open] \n    Scanning Port... \n"))  # term.green_on_black
            time.sleep(0.4)
        inp = input('Select a port to scan: ')
        inp = int(inp)
        if inp in ports:
            output = random.choice(outputs)
            time.sleep(3)
            clear_term()
            print(f'Port {inp} attackable. \n    Attack launchend. \n    Output: {output} \n')

        else:
            print('nothing')