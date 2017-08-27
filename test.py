import mcp23s17

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

