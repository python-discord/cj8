from blessed import terminal

def createDir(file_system, indent=0):
    for key, value in file_system.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            #INDENT BY 1 IF THE FILE IS A DIRECTORY
            createDir(value, indent+1)
        elif isinstance(value, list):
            for item in value:
                #PRINT LISTS IN A COLUMN
                print('\t' * (indent+1) + str(item))
        else:
            #PRINT NON DICTIONARY FILES AS THEY ARE
            print('\t' * (indent+1) + str(value))


# example nested dictionary for whole os directory
file_system = {
        "home": dict(
            {
                "user1":{
                            "home": list(['txt','txt2'])
                        },
                "user2":{
                            "home": list(['txt','txt2'])
                        }
            }
        ),
        "usr": dict(
            {
                "IDK":  {
                            "data": list(['txt','txt2'])
                        },
                "lib":  {
                            "lib_data": list(['txt','txt2'])
                        }
            }
        )
}

createDir(file_system)
