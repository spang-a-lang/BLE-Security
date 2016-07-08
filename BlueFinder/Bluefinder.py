#!/bin/python

import time
import binascii
import os
import signal
from scapy.all import *

def main():
	s = bindsock()

	LEsetscan(s, "00", "00")

	if sys.argv[1] == "-b":
		btle(s)
	if sys.argv[1] == "-c":
		BD_Addr = sys.argv[2]
		BD_Addr = BD_Addr.replace(":", "")
		BD_Addr = bytearray.fromhex(BD_Addr)
		BD_Addr.reverse()
		BD_Addr = binascii.hexlify(BD_Addr)

		clas_connect(s, BD_Addr)
		time.sleep(2)

		while True:
			RSSI = []
			while len(RSSI) < 50:
				data = s.recv()
				data = repr(data)

				# ping
				raw = bytearray.fromhex("020b0034003000010008c82c004142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f60616263646566676841424344")
				s.send(raw)
				time.sleep(.01)
				rssi(s)

				for line in data.splitlines():
					for part in line.split():
						if "load='\\x0b" in part:
							new = part[10:18]
							new = new.replace("\\x", "")
							RSSI.append(s16(int(("0x"+new),16)))
							#print(new)
						#print part
			dist(RSSI, 0)
	else:
		print("invalid input")

	disconnect(s)
	
def s16(value):
    return -(value & 0x80) | (value & 0x7f)

# btle
def btle(s):
	LEsetscanparam(s, "01")
	LEsetscan(s, "01", "00")
	while True:
		RSSI = []
		BD_Addr = []
		while len(RSSI) < 50:
			data = s.recv()
			data = repr(data)

			for line in data.splitlines():
				for part in line.split():
					if "addr=" in part:
						BD_Addr.append(part[5:22])
					if "load=" in part:
						RSSI.append(s16(int(part[8:10],16)))

			for i, item in enumerate(BD_Addr):
				input_addr = sys.argv[2]
				if item.lower() != input_addr.lower():
					del RSSI[i]
					del BD_Addr[i]

		dist(RSSI, -60)
	LEsetscan(s, "00", "00")

def dist(RSSI, int_RSSI):
	distance=[]

	# RSSI from bash script and convert to floating point
	#for element in sys.argv[2:]:
	#	RSSI.append(element)
	RSSI=map(float, RSSI)

	# calculate distance
	for i in RSSI[0:]:
		distance.append(round(10**((int_RSSI - i)/20),1))
		#print "%r" % (i)

	#for n in distance[0:]:
	#	print "%r m" % (n)
	avgdistance = round(sum(distance) / float(len(distance)),1)
	#for n in distance[0:]:
	#	print "%r m" % (n)
	print "%r m" % (avgdistance)

def clas_connect(BT_conn, addr):
	HCI_packet_type = "01"
	opcode = "0504"
	param_length = "0d"
	addr = addr
	packet_type = "18cc"
	page_scan_rep = "02"
	page_scan = "00"
	clock_offset = "0000"
	role = "01"

	raw = HCI_packet_type + opcode + param_length + addr + packet_type + page_scan_rep + page_scan + clock_offset + role
	#print raw
	raw = bytearray.fromhex(raw)
	BT_conn.send(raw)
	time.sleep(.5)

def LEsetscan(s, scan_enable, filter_dub):
	HCI_packet_type = "01"
	set_scan = "0c20"
	param_length = "02"
	scan_enable = scan_enable
	filter_dub = filter_dub

	raw = HCI_packet_type + set_scan + param_length + scan_enable + filter_dub
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)

def LEsetscanparam(s, scan_type):
	HCI_packet_type = "01"
	scan_param = "0b20"
	param_length = "07"
	scan_type = scan_type
	scan_interval = "1000"
	scan_window = "1000"
	own_addr = "00"
	scan_filter = "00"

	raw = HCI_packet_type + scan_param + param_length + scan_type + scan_interval + scan_window + own_addr + scan_filter
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)

def bindsock():
	output = subprocess.check_output(['bash','-c', "hciconfig hci0 down"])
	BT_conn = BluetoothUserSocket()
	return BT_conn
	time.sleep(.5)

def rssi(s):
	ran = bytearray.fromhex("010514020b00")
	s.send(ran)
# classic

# def classic_dist():
# 	RSSI=[]
# 	distance=[]

# 	# RSSI from bash script and convert to floating point
# 	for element in sys.argv[2:]:
# 		RSSI.append(element)
# 	RSSI=map(float, RSSI)

# 	# calculate distance
# 	for i in RSSI[0:]:
# 		distance.append(round(10**((-2 - i)/20),1))
# 		#print "%r" % (i)


# 	avgdistance = round(sum(distance) / float(len(distance)),1)
# 	#for n in distance[0:]:
# 	#	print "%r m" % (n)
# 	print "%r m" % (avgdistance)


if __name__ == "__main__":
	    main()