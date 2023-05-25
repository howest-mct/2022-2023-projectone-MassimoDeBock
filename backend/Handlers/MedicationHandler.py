from RPi import GPIO
from helpers.Class_TouchSensor import TouchSensor
from helpers.Class_Keypad import Keypad
import time
from helpers.Class_TimedFunction import TimedFunction
from helpers.Class_TimeOutableFunction import TimeOutableFunction

from repositories.DataRepository import DataRepository
from helpers.Class_RFID import TagReader


class MedicationHandler:
    def __init__(self):
        self.__timedFuncTouchSensor = TimedFunction(0.2)
        self.__touch = TouchSensor(16)
        self.__kPad = Keypad(6, 13, 19, 26, 0x20, 0, 1, 2, 3)
        self.__timedFuncRFID = TimedFunction(0.2,1)
        self.__timeOutFuncRFID = TimeOutableFunction()
        self.__rfidReader = TagReader()




    def update(self):
        self.__HandleKeyPad()
        self.__timedFuncTouchSensor(self.__HandleTouchSensor)
        self.__timedFuncRFID(self.__HandleReader)

    def __HandleTouchSensor(self):
        #print(f"touch: {self.__touch.CheckState()}")
        if (self.__touch.CheckJustPressed()):
            print(DataRepository.GetNextScheduledMedication())
            DataRepository.LogComponents(3,1)
            pass
    
    def __HandleKeyPad(self):
        if self.__kPad.Handle() ==1:
            code = self.__kPad.Code()
            print(code)
            self.__kPad.ResetCode()
            login = DataRepository.LoginAny(code)
            print(login)
            if login == None:
                DataRepository.LogComponents(4,-1)
            else:
                DataRepository.LogComponents(4,login)

    def __HandleReader(self):
        self.__timeOutFuncRFID(self.__ReadRFID)


    def __ReadRFID(self):
        if self.__rfidReader.Read():
            print(self.__rfidReader.getId())
            
            self.__timeOutFuncRFID.Timeout(2)
