#!/usr/bin/python
from scapy.all import * # Lazy import of scapy stuff
import crc16
import struct
import argparse
from spangslelib import *

# Open the file we want to read from
def readFirmwareFile(firmware_file):
    try:
        in_file = open(firmware_file,'rb')
        contents = in_file.read()
        in_file.close()
    except:
        print 'Cannot open firmware file... quitting now!'
        sys.exit()
    return contents

# Calculate the 16-bit CRC used by DFU
def calculateCRC(data):
    crc = crc16.crc16xmodem(data,0xffff)
    return format(crc & 0xffff, '04X')

# Calculate little endian size
def calculateSize(data):
    size = len(data)
    return binascii.hexlify(struct.pack('<I',size))

# Reverse byte order in hex string
def reverseBytes(in_string):
    out_string = ''
    in_string = binascii.unhexlify(in_string)
    for byte in in_string: out_string = byte + out_string
    return binascii.hexlify(out_string)

# Action that tells us when to stop sniffing
def stopSniff(packetType):
    def respConnectRequest(packet): # 1
        # Determine if connection was successful
        data = binascii.hexlify(packet[1].build())
        if data[0:2]=='3e':
            con_status = binascii.hexlify(packet[2].build())
            if con_status[0:2]=='01': # Connection successful
                return True
        return False
    def respWaitForWriteResp(packet): # 2
        # Use for first packet tx, and auth req tx
        data = binascii.hexlify(packet[0].build())
        if data[len(data)-6:len(data)]=='040013': # Write response detected
            global timed_out
            timed_out = False
            return True # stop sniffing
        return False
    def respWaitForNotification(packet): # 3
        try:
            data = binascii.hexlify(packet[3].build())
            if data[0:6]=='1b1000': # Notification detected
                if data[0:10] == '1b10001007' \
                or data[0:8] == '1b100011': # Special notifications
                    global tot_tx
                    tot_tx = int(reverseBytes(data[len(data)-8:len(data)]),16)
                    print 'Total transferred up to now: '+ str(tot_tx)
                return True
        except IndexError: data =''
        return False
    
    if packetType == 1: return respConnectRequest
    elif packetType == 2: return respWaitForWriteResp
    elif packetType == 3: return respWaitForNotification
    
    # If all else fails, do nothing.
    return

# Full script to upload firmware, first we set the device to DFU mode,
# then we send the firmware file using Nordic's legacy DFU OTA protocol
def updateFirmware(hci_socket,btaddr,contents,password):
   
    # Define the connect and disconnect packets
    connect_cmd=craftConnectReq(btaddr,'random')
    disconnect_cmd=craftDisconnectReq()

    # Connect to MX1101 and set it to DFU mode
    print 'Connecting to ' + btaddr + '...'
    hci_socket.send(connect_cmd)
    hci_socket.sniff(stop_filter=stopSniff(1)) # Connection request response
    hci_socket.send(craftWriteReq(0x001a,'0100'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response

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
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response

    # Put the device in DFU mode
    hci_socket.send(craftWriteReq(0x0019,'0101080405000000000000'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteReq(0x0019,'0101080108550000000000'))

    # Wait for some time, then reconnect with the device - it should be in DFU mode
    time.sleep(3)

    # Now in DFU mode, send firmware file
    hci_socket.send(connect_cmd)
    hci_socket.sniff(stop_filter=stopSniff(1)) # Connection request response
    hci_socket.send(craftWriteReq(0x000b,'0200'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteReq(0x0011,'0100'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteReq(0x0010,'01'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteCmd(0x000e,calculateSize(contents))) # SIZE of firmware
    hci_socket.sniff(stop_filter=stopSniff(3)) # Wait for notification
    hci_socket.send(craftWriteReq(0x0010,'02'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteCmd(0x000e,reverseBytes(calculateCRC(contents)))) # INIT params of firmware
    hci_socket.sniff(stop_filter=stopSniff(3)) # Wait for notification
    hci_socket.send(craftWriteReq(0x0010,'081900')) # 25 packets per burst
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteReq(0x0010,'03'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
    hci_socket.send(craftWriteReq(0x0010,'03'))
    hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response

    # Send data in sets of 25 packets, with 20 bytes each
    tot = len(contents)
    global tot_tx
    tot_tx = 0
    pkt_ct = 0
    global timed_out
    timed_out = False
    while (tot_tx < tot):
        # Grab up to 20 bytes from file
        try: 
            packet = contents[tot_tx:tot_tx+20]
        except: packet = contents[tot_tx:len(contents)]
        hci_socket.send(craftWriteCmd(0x000e,binascii.hexlify(packet))) # INIT params of firmware
        print binascii.hexlify(packet)
        tot_tx += len(packet)
        pkt_ct += 1

        if pkt_ct == 25 and tot_tx < tot:
            print 'Batch done: ' + str(tot_tx) + ' of ' + str(tot)
            hci_socket.sniff(stop_filter=stopSniff(3),timeout=2) # Wait for notification
            # Use this instruction to detect a timeout:
            hci_socket.send(craftWriteReq(0x0010,'03'))
            timed_out = True
            hci_socket.sniff(stop_filter=stopSniff(2),timeout=2) # Wait for write resp
            if timed_out: 
                print 'Time out detected.. attempting to reconnect'
                hci_socket.send(connect_cmd)
                hci_socket.sniff(stop_filter=stopSniff(1)) # Connection request response
                hci_socket.send(craftWriteReq(0x000b,'0200'))
                hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
                hci_socket.send(craftWriteReq(0x0011,'0100'))
                hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
                hci_socket.send(craftWriteReq(0x0010,'081900')) # 25 packets per burst
                hci_socket.sniff(stop_filter=stopSniff(2)) # Wait for write response
                hci_socket.send(craftWriteReq(0x0010,'07')) # Ask for received img size
                hci_socket.sniff(stop_filter=stopSniff(3)) # Wait for notification
            pkt_ct = 0

        time.sleep(.03)

    print 'Upload complete.'
    time.sleep(2)
    hci_socket.sniff(stop_filter=stopSniff(3)) # Wait for notification
    hci_socket.send(craftWriteReq(0x0010,'04'))
    hci_socket.sniff(stop_filter=stopSniff(3)) # Wait for notification
    hci_socket.send(craftWriteReq(0x0010,'05'))

    time.sleep(1)
    print 'Stopping...'
    time.sleep(1)
    hci_socket.send(disconnect_cmd)
    time.sleep(1)

    hci_socket.close()

    os.system("hciconfig hci0 down")

def parseargs():
    parser = argparse.ArgumentParser(
            description='Upload firmware to the BLE radio on an MX1101 data \
                        logger using Nordic Semiconductor\'s legacy DFU OTA \
                        protocol.')
    parser.add_argument('-b', '--btaddress', required=True, help='BLE device address')
    parser.add_argument('-f', '--file', required=True, help='Firmware file to upload')
    parser.add_argument('-p', '--password', help='Device password (if \
                        enabled)',default='')
    return parser.parse_args()

def main():
   
    # Grab target address and firmware filename
    args = parseargs()
    btaddr = args.btaddress
    firmware_file = args.file
    password = args.password

    # Set up sockets
    hci_socket = openBTSocket()
    contents = readFirmwareFile(firmware_file)

    # Load it up!
    updateFirmware(hci_socket,btaddr,contents,password)

if __name__ == "__main__":
    main()
    sys.exit(1)
