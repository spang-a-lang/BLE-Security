#! /usr/bin/Python
import sys
import os
import glob
import string

# select classic or btle calculation
sel = sys.argv[1]

# btle
if sel == "B":
	RSSI=[]
	distance=[]

	# RSSI from bash script and convert to floating point
	for element in sys.argv[2:]:
		RSSI.append(element)
	RSSI=map(float, RSSI)

	# calculate distance
	for i in RSSI[0:]:
		distance.append(round(10**((-60 - i)/20),1))
		#print "%r" % (i)

	#for n in distance[0:]:
	#	print "%r m" % (n)
	avgdistance = round(sum(distance) / float(len(distance)),1)
	#for n in distance[0:]:
	#	print "%r m" % (n)
	print "%r m" % (avgdistance)

# classic
else:
	RSSI=[]
	distance=[]

	# RSSI from bash script and convert to floating point
	for element in sys.argv[2:]:
		RSSI.append(element)
	RSSI=map(float, RSSI)

	# calculate distance
	for i in RSSI[0:]:
		distance.append(round(10**((-2 - i)/20),1))
		#print "%r" % (i)


	avgdistance = round(sum(distance) / float(len(distance)),1)
	#for n in distance[0:]:
	#	print "%r m" % (n)
	print "%r m" % (avgdistance)
