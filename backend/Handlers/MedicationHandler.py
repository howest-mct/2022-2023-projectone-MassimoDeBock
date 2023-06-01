from RPi import GPIO
from helpers.Class_TouchSensor import TouchSensor
from helpers.Class_Keypad import Keypad
import time
from helpers.Class_TimedFunction import TimedFunction
from helpers.Class_TimeOutableFunction import TimeOutableFunction

from repositories.DataRepository import DataRepository
from helpers.Class_RFID import TagReader

import datetime


class MedicationHandler:
    def __init__(self):
        self.__timedFuncTouchSensor = TimedFunction(0.2)
        self.__touch = TouchSensor(16)
        self.__kPad = Keypad(6, 13, 19, 26, 0x20, 0, 1, 2, 3)
        self.__timedFuncRFID = TimedFunction(0.2, 1)
        self.__timeOutFuncRFID = TimeOutableFunction()
        self.__rfidReader = TagReader()

        self.__lampPin = 21
        GPIO.setup(self.__lampPin, GPIO.OUT)
        self.__dosisReady = False

        self.__scannedCallback = None
        self.__rfidCallbackId = False

        self.__nextMedication = None

        self.__canDropWithTouch = True

        GPIO.output(self.__lampPin, False)

        self.__dataUpdateCallback = None

    def __del__(self):
        GPIO.output(self.__lampPin, False)

    def update(self):

        self.__HandleKeyPad()
        self.__timedFuncTouchSensor(self.__HandleTouchSensor)
        self.__timedFuncRFID(self.__HandleReader)
        self.HandleNextMedication()

    def __HandleTouchSensor(self):
        # print(f"touch: {self.__touch.CheckState()}")
        if (self.__touch.CheckJustPressed()):
            print(DataRepository.GetNextScheduledMedication())
            DataRepository.LogComponents(3, 1)

            if (self.__canDropWithTouch):
                self.DepositeMedication()
            pass

    def __HandleKeyPad(self):
        if self.__kPad.Handle() == 1:
            code = self.__kPad.Code()
            print(code)
            self.__kPad.ResetCode()
            login = DataRepository.LoginAny(code)
            print(login)
            if login == None:
                DataRepository.LogComponents(4, -1)
            else:
                DataRepository.LogComponents(4, login)

    def __HandleReader(self):
        self.__timeOutFuncRFID(self.__ReadRFID)

    def __ReadRFID(self):
        if self.__rfidReader.Read():
            id = self.__rfidReader.getId()
            print(id)
            if (self.__rfidCallbackId and (self.__scannedCallback != None)):
                self.__scannedCallback(id, self.__rfidCallbackId)
                self.__rfidCallbackId = None

            self.__timeOutFuncRFID.Timeout(2)

    def SetScanReturn(self, callback):
        self.__scannedCallback = callback

    def SetDataUpdateReturn(self, callback):
        self.__dataUpdateCallback = callback

    def SetScanReturnId(self, id):
        self.__rfidReader.reset()
        self.__rfidCallbackId = id

    def HandleNextMedication(self):
        if (self.__nextMedication == None):
            self.__nextMedication = DataRepository.GetNextScheduledMedication()
        elif (self.__dosisReady):
            GPIO.output(self.__lampPin, True)

        elif (self.__nextMedication["Time"] < datetime.datetime.now()):
            self.__dosisReady = True
            DataRepository.SetNextDropActive()
            print("new dosis ready")
            self.__nextMedication = DataRepository.GetNextScheduledMedication()
            print(self.__nextMedication)
            self.__dataUpdateCallback()
        else:
            GPIO.output(self.__lampPin, False)

    def DepositeMedication(self):
        if (self.__nextMedication["Status"] == "InProgress"):
            DataRepository.SetActiveDropTaken()
            self.__nextMedication = None
            print("vroom vroom medication being dropped weee")
            self.__dataUpdateCallback()
            self.__dosisReady = False
