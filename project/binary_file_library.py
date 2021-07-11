#FILE ENCRYPTION LIBRARY - DEVELOPED BY CHEERFUL CHEETAHS (Contributed by Coder400, [PUT YOUR NAME HERE])
import string

#Create our table of all characters.
ALL_CHARACTERS = string.ascii_letters+string.digits+string.punctuation+string.whitespace

#Define our XOR operator.
def XOR(a, b):
    return (a and not b) or (not a and b)

def caesar_cipher(characters, msg, shift, reverse=False):
    encrypted_msg = ""
    #If reversed, make the factor negative.
    factor = 1
    if reverse:
        factor = -1
    #for each character in message.
    for character in msg:
        #Find character, shift it and then add it to the message.
        character_index = characters.index(character)
        encrypted_msg += characters[(character_index+(shift*factor))%len(characters)]
    #Return the encrypted message
    return encrypted_msg

#Calculate the value of our hash.
def getHashValue(password):
    #Initialise our value to 0.
    value = 0
    for character in password:
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

def modify(byte_array, password):
    for pos,byte in enumerate(byte_array):
        #Go into each pos and run XOR on current byte and our HASH
        byte_array[pos] = XOR(byte, getHashValue(password))
    return byte_array

# Function to encrypt/decrypt files for the OS. (We only need 1 function because of XOR cipher)
def modifyFile(filename, password):
    #Get our bytes to work with and then modify them.
    data_bytes = modify(generate_Bytearray(filename), password)
    file = open(filename, 'wb')
    file.truncate()
    file.write(data_bytes)
    file.close()

def openFile(filename, shift, password):
    global ALL_CHARACTERS
    #Get decrypted bytes.
    data_bytes = modify(generate_Bytearray(filename), password)
    #Decode our message from bytes to a readable format.
    msg = data_bytes.decode('utf-8')
    #Decrypt the message retrieved.
    msg = caesar_cipher(ALL_CHARACTERS, msg, shift, reverse=True)
    return msg

def writeFile(filename, msg, shift, password):
    global ALL_CHARACTERS
    #Create file on our system.
    file = open(filename, 'x')
    file.close()
    file = open(filename, 'wb')
    #Add caesar cipher to the msg
    msg = caesar_cipher(ALL_CHARACTERS, msg, shift)
    #Convert our message into bytes
    msg = bytes(msg, 'utf-8')
    msg = bytearray(msg)
    #Write bytes into file and then close.
    file.write(msg)
    file.close()
    #Encrypt our file.
    modifyFile(filename, password)
