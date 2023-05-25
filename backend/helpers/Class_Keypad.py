from RPi import GPIO
from smbus import SMBus


class Keypad:

    def __init__(self, row0: int, row1: int, row2: int, row3: int, addressPCF: int, col0: int, col1: int, col2: int, col3: int):
        self.__rows = [row0, row1, row2, row3]
        self.__cols = [1 << col0, 1 << col1, 1 << col2, 1 << col3]
        self.__pcfFilter = self.__cols[0] | self.__cols[1] | self.__cols[2] | self.__cols[3]
        self.__values = [1, 4, 7, '*',
                         2, 5, 8, 0,
                         3, 6, 9, '#',
                         'A', 'B', 'C', 'D', '?']  # the ? is an error, should normaly not be possible unless this code happened too slowly
        self.__shouldCheck = False
        self.__address = addressPCF
        self.__bus = SMBus(1)
        self.__buffer = []

        GPIO.setmode(GPIO.BCM)

        for x in self.__rows:
            GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(
                x, GPIO.RISING, callback=self.__KeypadInteract, bouncetime=200)

    def __KeypadInteract(self, channel):
        self.__shouldCheck = True

    def __WritePCF(self, prevState, bits):
        self.__bus.write_byte(self.__address, prevState |
                              (bits & self.__pcfFilter))

    def Handle(self) -> int:
        if self.__shouldCheck:
            self.__shouldCheck = False
            prev = self.__bus.read_byte(
                self.__address) & (self.__pcfFilter ^ 255)
            hit = self.__CheckAllButtons(prev)
            self.__WritePCF(prev, self.__pcfFilter)
            value = self.__values[hit]
            if value == '?':
                return -2
            if value == '#':
                print(f"Code entered:")
                # print(*(self.__buffer), sep='')
                return 1
            if value == '*':
                self.__buffer.clear()
                print(f"Buffer cleared")
                return -1
            self.__buffer.append(value)
            if(self.__buffer.__len__()>3):
                return 1
            # print(*(self.__buffer), sep='')

        return 0
    
    def Code(self):
        input = ''
        for char in self.__buffer:
            input += str(char)
        return input
    
    def ResetCode(self):
        self.__buffer.clear()
        print(f"Buffer cleared")

    def __CheckAllButtons(self, prev):
        counter = 0
        for x in self.__cols:
            self.__WritePCF(prev, x)
            for y in self.__rows:
                if GPIO.input(y):
                    return counter

                else:
                    counter += 1
        return 16
