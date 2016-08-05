#!/usr/bin/python

from scapy.all import * # Lazy import of scapy stuff
import binascii
import os

# Create socket to communicate with BT device
def openBTSocket():
    os.system("hciconfig hci0 down")
    try:
        hci_socket = BluetoothUserSocket()
    except BluetoothSocketError:
        print 'Cannot bind to Bluetooth socket... quitting now!'
        sys.exit()
    return hci_socket

# Craft a write request, scapy-style
def craftWriteReq(handle,data):
    wr=ATT_Write_Request(gatt_handle=handle,data=binascii.unhexlify(data))
    att=ATT_Hdr(opcode=0x12)/wr
    l2c=L2CAP_Hdr(cid=0x0004,len=len(att))/att
    acl=HCI_ACL_Hdr(handle=0x040,len=len(l2c))/l2c
    hci=HCI_Hdr(type=2)/acl
    return hci

# Craft a write command, scapy-style
def craftWriteCmd(handle,data):
    wr=ATT_Write_Request(gatt_handle=handle,data=binascii.unhexlify(data))
    att=ATT_Hdr(opcode=0x52)/wr
    l2c=L2CAP_Hdr(cid=0x0004,len=len(att))/att
    acl=HCI_ACL_Hdr(handle=0x040,len=len(l2c))/l2c
    hci=HCI_Hdr(type=2)/acl
    return hci

def craftConnectReq(btaddr,random):
    return HCI_Hdr()/HCI_Command_Hdr()/\
            HCI_Cmd_LE_Create_Connection(paddr=btaddr,patype=random)

def craftDisconnectReq():
    return HCI_Hdr()/HCI_Command_Hdr(opcode=0x0406,len=3)/\
            binascii.unhexlify('400013')
