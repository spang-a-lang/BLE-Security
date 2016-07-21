#!/bin/python

import time
import binascii
import os
import threading
import signal
from scapy.all import *

def main():
	user_input = [None]
	s = bindsock()
	LEsetscan(s, "00", "00")

	mythread = threading.Thread(target=get_user_input, args=(user_input,))
	mythread.daemon = True
	mythread.start()

	if len(sys.argv) == 1:
		print '\n' + "                      BlueFinder v1.3a"
	 	print "      python BlueFinder.py <sel> <-l> <Ant> <BD_Addr>"
		print '\n\n' + "                     DESCRIPTION"
  		print "         <sel>              -c - Classic, -b - Low-Energy"
  		print "          <-l>              Long-range mode for use with UD-100 (optional)"
  		print "         <Ant>              Antenna Gain [3, 9, 15]             (optional)"
		print "       <BD_Addr>            Bluetooth Device Address"


	elif len(sys.argv) == 3:
		if sys.argv[1] == "-b":
			btle(s, sys.argv[2], user_input, -60)
		elif sys.argv[1] == "-c":
			classic(s, user_input)
		else:
			print("Error: invalid selection")

	elif len(sys.argv) == 5:
		if sys.argv[3] == "3":
			btle(s, sys.argv[4], user_input, -26)
		elif sys.argv[3] == "9":
			btle(s, sys.argv[4], user_input, -24)
		elif sys.argv[3] == "15":
			btle(s, sys.argv[4], user_input, -22)
		else:
			print("Error: invalid gain")

	else:
			print("Error: invalid input")

	disconnect(s)
	sys.exit()
	return(s)

def get_user_input(user_input_ref):
    user_input_ref[0] = raw_input()

def classic(s, user_input):
	BD_Addr = sys.argv[2]
	BD_Addr = BD_Addr.replace(":", "")
	BD_Addr = bytearray.fromhex(BD_Addr)
	BD_Addr.reverse()
	BD_Addr = binascii.hexlify(BD_Addr)

	clas_connect(s, BD_Addr)
	time.sleep(2)

	while not keystop():
		try:
			RSSI = []
			while len(RSSI) < 100:
				data = s.recv()
				data = repr(data)

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
			dist(RSSI, 0)
		except KeyboardInterrupt:
				print "\nExiting BlueFinder"
				LEsetscan(s, "00", "00")
				disconnect(s)
				sys.exit()
				return()

def s16(value):
    return -(value & 0x80) | (value & 0x7f)

# btle
def btle(s, input_addr, user_input, int_RSSI):
	LEsetscanparam(s, "01")
	LEsetscan(s, "01", "00")
	
	while not keystop():
		try:
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
					if item.lower() != input_addr.lower():
						del RSSI[i]
						del BD_Addr[i]

			dist(RSSI, int_RSSI)

		except KeyboardInterrupt:
			print "\nExiting BlueFinder"
			LEsetscan(s, "00", "00")
			disconnect(s)
			sys.exit()
			return()


def dist(RSSI, int_RSSI):
	distance=[]
	RSSI=map(float, RSSI)
	for i in RSSI[0:]:
		#printtofile(i)			# enable if recording RSSI
		distance.append(round(10**((int_RSSI - i)/20),1))
	avgdistance = round(sum(distance) / float(len(distance)),1)
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

def disconnect(s):
	raw = "01060403400013"
	raw = bytearray.fromhex(raw)
	s.send(raw)

def printtofile(RSSI):
	f = open('1m.txt','a')
	f.write(str(RSSI) + ' ')
	f.close()

def keystop(delay = 0):
	return len(select.select([sys.stdin], [], [], delay)[0])

if __name__ == "__main__":
		while not keystop():
			try:
				main()
			except KeyboardInterrupt:
				print "\n Exiting BlueFinder"
			except IndexError:
				print "Error: Index"
			finally:
				sys.exit()
