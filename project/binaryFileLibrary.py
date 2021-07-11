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
    file = open(filename, 'rb')
    #Convert our bytes into a byte array.
    data = bytearray(file.read())
    file.close()
    return data

def modify(byte_array):
    for pos,byte in enumerate(byte_array):
        #Go into each pos and run XOR on current byte and our HASH
        byte_array[pos] = XOR(byte, HASH)
    return byte_array

# Function to encrypt/decrypt files for the OS. (We only need 1 function because of XOR cipher)
def modifyFile(filename):
    #Get our bytes to work with and then modify them.
    data_bytes = modify(generate_Bytearray(filename))
    file = open(filename, 'wb')
    file.truncate()
    file.write(data_bytes)
    file.close()

def openFile(filename):
    #Get decrypted bytes.
    data_bytes = modify(generate_Bytearray(filename))
    #Decode our message from bytes to a readable format.
    msg = data_bytes.decode('utf-8')
    return msg

def writeFile(filename, msg):
    #Create file on our system.
    file = open(filename, 'x')
    file.close()
    file = open(filename, 'wb')
    #Convert our message into bytes
    msg = bytes(msg, 'utf-8')
    msg = bytearray(msg)
    #Write bytes into file and then close.
    file.write(msg)
    file.close()
    #Encrypt our file.
    modifyFile(filename)
