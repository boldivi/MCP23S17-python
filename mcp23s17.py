#!/usr/bin/python

import time
import RPi.GPIO as GPIO

class MCP23S17():
	def __init__(self,MISO=9,MOSI=10,CLK=11,CS=8,RESET=5):
		self.ADDR = 0b0100000
		self.IODIRA	= 0x00
		self.IODIRB	= 0x01
		self.GPIOA	= 0x12
		self.GPIOB	= 0x13
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		self.MISO	= MISO
		self.MOSI	= MOSI
		self.CLK	= CLK
		self.CS		= CS
		self.RESET	= RESET
		GPIO.setup(self.MISO, GPIO.IN)
		GPIO.setup(self.MOSI, GPIO.OUT)
		GPIO.setup(self.CLK, GPIO.OUT)
		GPIO.setup(self.CS, GPIO.OUT)
		GPIO.setup(self.RESET, GPIO.OUT)
		self.Reset()
		self.CsHigh()
		self.ClkLow()
		self.MosiLow()
		self.WriteReg(self.IODIRB,0)
	def Reset(self):
		GPIO.output(self.RESET,False)
		time.sleep(0.1)
		GPIO.output(self.RESET,True)
		time.sleep(0.1)
	def CsLow(self):
		GPIO.output(self.CS,False)
	def CsHigh(self):
		GPIO.output(self.CS,True)
	def ClkLow(self):
		GPIO.output(self.CLK,False)
	def ClkHigh(self):
		GPIO.output(self.CLK,True)
	def MosiLow(self):
		GPIO.output(self.MOSI,False)
	def MosiHigh(self):
		GPIO.output(self.MOSI,True)
	def SpiSend(self,data):
		for i in range(8):
			if data & 0b10000000:
				self.MosiHigh()
			else:
				self.MosiLow()
			time.sleep(0.001)
			self.ClkHigh()
			time.sleep(0.001)
			self.ClkLow()
			time.sleep(0.001)
			data <<= 1
	def WriteReg(self,regaddr,data):
		IC_addr = (self.ADDR << 1) | 0
		REG_addr = regaddr
		self.CsLow()
		self.SpiSend(IC_addr)
		self.SpiSend(REG_addr)
		self.SpiSend(data)
		self.CsHigh()

	def ReadReg(self,regaddr):
		# IC_addr = 0b01000001
		IC_addr = (self.ADDR << 1) | 1
		REG_addr = regaddr
		self.CsLow()
		self.SpiSend(IC_addr)
		self.SpiSend(REG_addr)
		data = 0
		for i in range(8):
			data = data << 1
			if GPIO.input(self.MISO) == True:
				data |= 1
			else:
				data &= ~1
			self.ClkHigh()
			time.sleep(0.001)
			self.ClkLow()
			time.sleep(0.001)
		self.CsHigh()
		return data
	def DirGIPOA(self,value):
		self.WriteReg(self.IODIRA,value)
	def DirGIPOB(self,value):
		self.WriteReg(self.IODIRB,value)
	def ReadGPIOA(self):
		return self.ReadReg(self.GPIOA)
	def WriteGPIOA(self,value):
		self.WriteReg(self.GPIOA,value)
	def ReadGPIOB(self):
		return self.ReadReg(self.GPIOB)
	def WriteGPIOB(self,value):
		self.WriteReg(self.GPIOB,value)

'''
# Initialize default GPIO map: MISO=9,MOSI=10,CLK=11,CS=8,RESET=5
io = MCP23S17()

# Init Examples:
# io = MCP23S17(MISO=9,MOSI=10,CLK=11,CS=8,RESET=5)
# io = MCP23S17(9,10,11,8,5)

#io.WriteReg(1,0)

# Set all GPIOA pin to output
io.DirGIPOA(0xff)

# Set all GPIOB pin to output
io.DirGIPOB(0x00)

while 1:
	io.WriteGPIOB(0x55)
	time.sleep(1)
	io.WriteGPIOB(0xaa)
	time.sleep(1)
	print bin(io.ReadGPIOA())

	print io.ReadReg(0x12)
	io.WriteReg(0x13,0x55)
	time.sleep(1)
	io.WriteReg(0x13,0)
	time.sleep(1)
'''
