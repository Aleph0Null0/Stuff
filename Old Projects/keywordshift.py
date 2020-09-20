#----------------------------------------------------------------
#Program Name: Keyword Shift
#Programmer: Arya Hosseini
#Date: February 22, 2019
#Input: a key and a message from a text file the program opens
#Processing: The message is capitalized and each alphabetical
#            character is shifted through the alphabet by the
#            number in the alphabet that its corresponding
#            letter within the key is positioned
#Output: After each letter is shifted the coded message is
#        outputted in the python shell
#----------------------------------------------------------------
file = open('input.txt','r')
fileContents = [i.strip() for i in file.readlines()]
def keywordShift(key,message): #Function taking two strings and encoding the second based on the first
    key = ''.join([i.upper() for i in key if i.isalpha()]) #Capitalizing and removing non-alpha characters
    message = ''.join([i.upper() for i in message if i.isalpha()]) 
    ords = [ord(letter) for letter in message] 
    shifts = [(ord(letter)-65) for i,letter in enumerate(key)]
    newOrds = [(ord(message[i])+shifts[i%len(key)]) for i,ordinate in enumerate(ords)] #Shifting each ordinal from the message
    newOrds = [i - 26 if i > 90 else i for i in newOrds] #Cycling back through the alphabet if the shift pushes the ordinal value too high
    encryption = ''.join([chr(i) for i in newOrds])
    return encryption
for i in range(len(fileContents)): #Iterating through the given file by a line by line, key, message, pattern
    if i%2 == 0:
        print(keywordShift(fileContents[i],fileContents[i+1]))
