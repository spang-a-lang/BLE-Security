#!/usr/bin/python
from scapy.all import * # Lazy import of scapy stuff
import binascii
import os
import argparse
from spangslelib import *

# Response for sniffed packets
def sniffResp(packet):
    global outfile
    try:
        data = binascii.hexlify(packet[4].build()) # 4th layer,1st pack
        data = data[4:len(data)] # take out first 4 chars (2 bytes)
        # Do something special with the first and last packets!
        if outfile:
            if data[0:2]=='01': 
                # print 'First'
                # Skip first 5 bytes of first packet
                outfile.write(binascii.unhexlify(data[10:len(data)]))
            elif data[0:2]=='6d': 
                global done
                done = True
                #print 'Last!', do not print 6d!
            else: outfile.write(binascii.unhexlify(data[2:len(data)]))
        if screen_feed: print data
    except IndexError: # Handle but do nothing
        return

# Action that tells us when to stop sniffing
def stopSniff(packet):
    try:
        data = binascii.hexlify(packet[4].build()) # 4th layer,1st pack
        data = data[4:len(data)-1] # take out first 4 chars (2 bytes)
    except IndexError:
        return False
    return data[0:2]=='6d'

def extractData(hci_socket,btaddr,start_address,stop_address,password):
    hci_socket.send(craftConnectReq(btaddr,'random'))
    hci_socket.sniff(count=2) # 2 responses for connection

    hci_socket.send(craftWriteReq(0x001a,'0100'))
    hci_socket.sniff(count=2)

    # Generate authentication request (send password)
    if password == '':
        pass_message = '010104051c0100'
    else:
        password = binascii.hexlify(password)
        # Zero pad to 10 bytes (20 'spots')
        while len(password) < 20:
            password += '00'
        if len(password) > 20:
            print 'Password '+binascii.unhexlify(password)+\
                    ' is too long! Truncating...'
            password=password[0:20]
        pass_message = '01010d051c01'+password+'00'

    hci_socket.send(craftWriteReq(0x0019,pass_message))
    hci_socket.sniff(count=3)
    
    hci_socket.send(craftWriteReq(0x0019,'0101080405000000000000'))
    hci_socket.sniff(count=4)

    # Determine range based on start and stop address - we go in steps of 2048
    # Round down by using AND
    start_address = start_address & 0xFFFFF000 # round down
    stop_address = (stop_address & 0xFFFFF000) + 2048 # round up, normalize
    if stop_address < start_address:
        print 'Invalid address range, end address should come after start!'
    else:
        for i in range(start_address/2048,stop_address/2048): # 0 to 2097152 to get everything
            address = '%0.8X' % (i*2048)
            print 'Dumping: 0x' + address + '-0x' + '%0.8X' % (i*2048 + 2047)
            hci_socket.send(craftWriteReq(0x0019,'01010a0a01'+address+'00000800'))
            # Unfortunately, sniff doesn't raise the KeyboardInterrupt exception,
            # so we'll come up with an alternate way to tell if we exited prematurely
            global done
            done = False
            hci_socket.sniff(count=0,prn=sniffResp,stop_filter=stopSniff)
            if not done: break # Uh-oh, something happened. Let's exit gracefully    

    print 'Stopping...'
    time.sleep(1)
    hci_socket.send(craftDisconnectReq())
    time.sleep(1)

def parseargs():
    parser = argparse.ArgumentParser(
            description='Extract arbitrary data from the MX1101 data logger. \
        This tool returns 2048-byte blocks, starting with the block that \
        contains the provided starting address and optionally ending with the \
        block containing the end address. If no end address is provided, the \
        tool returns a single block.')
    parser.add_argument('-b', '--btaddress', required=True, help='BLE device address')
    parser.add_argument('-s', '--startaddress', required=True,\
                        help='32-bit address in first desired address block')
    parser.add_argument('-e', '--endaddress',default='',\
                        help='32-bit address in last desired address block. If\
                        none given, we return a single block.')
    parser.add_argument('-o', '--outputfile',\
                        help='File to store output',default='')
    parser.add_argument('-p', '--password',\
                        help='Device password (if enabled)',default='')
    return parser.parse_args()

def main():
   
    # Grab target address and other parameters
    args = parseargs()
    btaddr = args.btaddress
    start_address = int(args.startaddress,16)
   
    stop_address = args.endaddress
    if stop_address=='':
        stop_address=start_address
    else:
        stop_address=int(stop_address,16)
    
    output_file = args.outputfile
    password = args.password

    global outfile
    # Open the file we want to write to
    if output_file != '':
        try:
            outfile = open(output_file,'w')
        except:
            print 'Cannot open file... quitting now!'
            sys.exit()

    # Set up sockets
    hci_socket = openBTSocket()

    # Pull it off!
    extractData(hci_socket,btaddr,start_address,stop_address,password)

    outfile.close()
    hci_socket.close()

if __name__ == "__main__":
    main()
    sys.exit(1)
