from RPi import GPIO
import time
import enum
from smbus import SMBus


class PCF:
    def __init__(self, address):
        self.__address = address
        self.__i2c: SMBus = SMBus()
        self.__i2c.open(1)

    def Invbit(self, bit):
        return ~bit & 0xff

    def Write(self, byte):
        self.__i2c.write_byte(self.__address, byte)

    def SetSpecificBits(self, valuableBits, byte):
        data = self.__i2c.read_byte(self.__address)
        data = (self.Invbit(valuableBits) & data) | (valuableBits & byte)
        self.__i2c.write_byte(self.__address, data)

    def GetBytes(self):
        return self.__i2c.read_byte(self.__address)