#!/bin/python

# Testing new things

import time
from scapy.all import *
from BTLE import *

def main():
   s = bindsock()
   
   # Spoof address
   # ran = bytearray.fromhex("01011000")
   # s.send(ran)
   # ran = bytearray.fromhex("0101fc06263dcfd5b370")
   # s.send(ran)
   # ran = bytearray.fromhex("01030c00")
   # s.send(ran)
   # time.sleep(.5)
   
   # change local name
   # ran = bytearray.fromhex("01130cf84269746c6f636b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
   # s.send(ran)
   # time.sleep(.5)

      # Set Event mask
   ran = bytearray.fromhex("01010c08fffffbff07f8bf3d")
   s.send(ran)
   time.sleep(.5)

      # Set LE Event mask
   ran = bytearray.fromhex("010120081f00000000000000")
   s.send(ran)
   time.sleep(.5)

      # Read Local Version
   ran = bytearray.fromhex("01011000")
   s.send(ran)
   time.sleep(.5)

      # Write LE Host Support
   ran = bytearray.fromhex("016d0c020100")
   s.send(ran)
   time.sleep(.5)

      # Read LE host support
   ran = bytearray.fromhex("016c0c00")
   s.send(ran)
   time.sleep(.5)

      # Read BD Addr
   ran = bytearray.fromhex("01091000")
   time.sleep(.5)

      # Set Adver Enable
   ran = bytearray.fromhex("010a200100")
   s.send(ran)
   time.sleep(.5)

      # Set LE Adver Param
   ran = bytearray.fromhex("0106200fa000a0000000000000000000000700")
   s.send(ran)
   time.sleep(.5)

      # Set LE Scan Resp
   ran = bytearray.fromhex("010920200a09083030303030643236000000000000000000000000000000000000000000")
   s.send(ran)
   time.sleep(.5)

      # Set LE Adver Data
   ran = bytearray.fromhex("0108202015020106110626ba93c026e4598fbb4d3428dffe3d6900000000000000000000")
   s.send(ran)
   time.sleep(.5)

      # Set Adver Enable
   ran = bytearray.fromhex("010a200101")
   s.send(ran)
   time.sleep(.5)

      # Set Scan Resp
   ran = bytearray.fromhex("010920200a09083030303030643236000000000000000000000000000000000000000000")
   s.send(ran)
   time.sleep(.5)

      # Set LE Adver Data
   ran = bytearray.fromhex("0108202015020106110626ba93c026e4598fbb4d3428dffe3d6900000000000000000000")
   s.send(ran)
   time.sleep(1)

   #  Send Write Resp
   #ran = bytearray.fromhex("02400005000100040013")
   #s.send(ran)


   time.sleep(30)

   # LE Set Advertise Disable
   #for i in range(1,99):
   ran = bytearray.fromhex("010a200100")
   s.send(ran)

   # UnSpoof address
   # ran = bytearray.fromhex("01011000")
   # s.send(ran)
   # ran = bytearray.fromhex("0101fc064509058A5898")
   # s.send(ran)
   # ran = bytearray.fromhex("01030c00")
   # s.send(ran)
   # time.sleep(.5)

   # Return name to normal
   # ran = bytearray.fromhex("01130cf84472656467000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
   # s.send(ran)

   # rand = "00"
   # Connect(s, "263DCFD5B370", rand)

   # readreq(s, "5100" )
   # readreq(s, "5300" )


   # # for i in range(1,16):
   # #    a = "0" + str('{0:x}'.format(int(i))) + "00"
   # #    #print(a)
   # #    readreq(s, a)

   # # for i in range(130,160):
   # #    a = str('{0:x}'.format(int(i))) + "00"
   # #    print(a)
   # #    readreq(s, a)

   # writereq(s, "2B00","0100")
   # writereq(s, "3200","0100")
   # writereq(s, "3800","0100")
   # writecmd(s, "2D00","26ba93c026e4598fbb4d3428dffe3d69")

   time.sleep(5)
   disconnect(s)

if __name__ == "__main__":
    main()