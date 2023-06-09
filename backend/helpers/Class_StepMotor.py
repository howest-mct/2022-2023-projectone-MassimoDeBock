from RPi import GPIO
from smbus import SMBus
import time


class StepMotor:

    def __init__(self, addressPCF: int):
        self.__address = addressPCF
        self.__bus = SMBus(1)
        self.__pcfFilter = 0b11110000
        self.__state = 0
        self.__bits = [0b1001, 0b0001, 0b0011,
                       0b0010, 0b0110, 0b0100, 0b1100, 0b1000]
        # tem 7

    def turn(self, change):
        direction = int(change/abs(change))
        for x in range(0, change, direction):
            self.__state = ((self.__state + direction)+8) % 8
            self.writePCF(self.__bits[self.__state])
            time.sleep(0.0003)
        self.writePCF(0)


    def writePCF(self, bits):
        bits = bits << 4
        prev = self.__bus.read_byte(self.__address) & (self.__pcfFilter ^ 255)
        self.__bus.write_byte(self.__address, prev |
                              (bits & self.__pcfFilter))

    def turnFull(self):
        self.StepMotor.turn(4080)
