from RPi import GPIO

class TouchSensor:

    def __init__(self, pin):
        self.__pin = pin
        self.__state = False
        self.__justPressed = False
        self.__justReleased = False


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.__pin, GPIO.BOTH, self.__Change, bouncetime=200)
        #GPIO.add_event_detect(self.__pin, GPIO.RISING, self.__Released, bouncetime=200)

        #GPIO.setup(self.__pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)



    def __Pressed(self, channel):
        self.__state = True
        self.__justPressed = True

    def __Released(self,channel):
        self.__state = False
        self.__justReleased = True

    def __Change(self, channel):
        state = GPIO.input(self.__pin)
        if state:
            self.__state = True
            self.__justPressed = True 
        else:
            self.__state = False
            self.__justReleased = True
        
        
    def CheckState(self) -> bool:
        return self.__state
    
    def ResetButton(self) -> None:
        self.__state = False

    def CheckJustPressed(self) -> bool:
        if self.__justPressed:
            self.__justPressed = False
            return True
        return False
    
    def CheckJustReleased(self) -> bool:
        if self.__justReleased:
            self.__justReleased = False
            return True
        return False