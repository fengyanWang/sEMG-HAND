# encoding=utf8 

from __future__ import print_function

import serial
import serial.tools.list_ports
import time

# from handPosition import myHandPosition

'''
The movement of the artificial hand is controlled by a serial port
'''
class mySerial(object):

	def __init__(self):

		self.serialName = "/dev/ttyUSB0"
		self.baudrate = 115200
		self.waitTime = 0.01
		self._initialize()
		self.recvCount = 0
		
	def _initialize(self):
		self.openSerial()
	
	def openSerial(self):
		self.port = serial.Serial(self.serialName, self.baudrate)
	
	def closeSerial(self):
		self.port.close()
	
	def findSerial(self):
		plist = list(serial.tools.list_ports.comports())
		for i in plist:
			plist_temp = list(i)
			print("A serial port as follows:" , plist_temp[0] )

		if len(plist) <= 0:
			print("No usable serial port was found, please make sure the device is connected！！")
		else:

			plist_0 = list(plist[0])
			self.serialName = plist_0[0]
			print("The serial number used is:" , self.serialName)
	
	def sendCmd(self,cmdStr):

		self.port.write(cmdStr)
		time.sleep(self.waitTime)
		self.port.flush()

	def recvCmd(self , cmdCount = 7):
		cmdList = []
		while True:
			self.recvCount += 1
			cmdList.append(ord(self.port.read()))
			if self.recvCount == cmdCount:
				return cmdList
				break

	def setWaitTime(self , myTime):
		self.waitTime = myTime

	def setBaudRate(self , myBaudRate):
		self.baudrate = myBaudRate

	def setSerialName(self , mySerialName):
		self.serialName = mySerialName

if __name__ == '__main__':
	pass



	

