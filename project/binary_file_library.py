#FILE ENCRYPTION LIBRARY - DEVELOPED BY CHEERFUL CHEETAHS (Contributed by Coder400, [PUT YOUR NAME HERE])
import string

HASH = "abcdef"

#Define our XOR operator.
def XOR(a, b):
    return (a and not b) or (not a and b)

#Function to edit current hash. (HIGHLY RECOMMENDED)
def editHash(newHash):
    global HASH
    HASH = newHash

#Calculate the value of our hash.
def getHashValue():
    #Initialise our value to 0.
    value = 0
    for character in HASH:
        #Add up the value of the character.
        value += ord(character)
    return value

#Get bytearray from file.
def generate_Bytearray(filename):
    file = bytes(filename)
    #Convert our bytes into a byte array.
    data = bytearray(file.read())
    file.close()
    return data

# Function to encrypt/decrypt files for the OS. (We only need 1 function because of XOR cipher)
def modifyFile(filename):
    #Get our bytes to work with.
    data_bytes = generate_Bytearray(filename)
    for pos,byte in enumerate(data_bytes):
        #Go into each pos and run XOR on current byte and our HASH
        data_bytes[pos] = XOR(byte, HASH)
    file = open(filename, 'wb')
    file.truncate()
    file.write(data_bytes)
    file.close()
