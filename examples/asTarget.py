# Example of running the PN532 as target(emulation mode)
# Author: Salvador Mendoza(salmg.net)
# More info: http://salmg.net/2019/02/15/chiptonfc-local-relay-sniffer

from smartcard.util import toHexString, toBytes
import PN532

# Configuration for a Raspberry Pi GPIO:
CS   = 8
MOSI = 10
MISO = 9
SCLK = 11

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

def printString(data1):
    out = ''
    for x in range(len(data1)):
		out += '%02x' % data1[x]
    return out

#----Credits to Adam Laurie(Major Malfunction)
def TargetConf():
	mode = '00'
	sens_res = '0800'
	uid = 'dc4420'
	sel_res = '60'
	felica = '01fea2a3a4a5a6a7c0c1c2c3c4c5c6c7ffff'
	nfcid =  'aa998877665544332211'
	last6 = '00'
	last7 = '52464944494f7420504e353332'
	data1 = '4006884501025442d24092010339000037556f'

	try:
		lengt= '%02x' % (len(last6) / 2)
		gt= last6
	except:
		lengt= '00'
		gt= ''
	try:
		lentk= '%02x' % (len(last7) / 2)
		tk= last7
	except:
		lentk= '00'
		tk= ''

	return mode+sens_res+uid+sel_res+felica+nfcid+lengt+gt+lentk+tk
#----
def sendAPDU(apdu):
	sendData = pn532.call_function(PN532.PN532_COMMAND_TGSETDATA,params=apdu)

def getAPDU():
	global apdu
	result = pn532.call_function(PN532.PN532_COMMAND_TGGETDATA,255)
	apdu = printString(result)[2:]
	return apdu

print "Checking PN532?"
pn532.begin()

# Get the firmware version from the chip and print(it out.)
ic, ver, rev, support = pn532.get_firmware_version()
print('-----\nFound PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()

#Initialize PN532 in target mode

print "-----\nInit As Target> "
runit = pn532.call_function(PN532.PN532_COMMAND_TGINITASTARGET,params=toBytes(TargetConf())) #prepareApdu(TargetConf()))

print "-----\nGet Data> ",
apdu = pn532.call_function(PN532.PN532_COMMAND_TGGETDATA,255)

print(apdu)
