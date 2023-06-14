from RPi import GPIO
from helpers.Class_TouchSensor import TouchSensor
from helpers.Class_Keypad import Keypad
import time
from helpers.Class_TimedFunction import TimedFunction

from repositories.DataRepository import DataRepository
from helpers.Class_RFID import TagReader
from helpers.Class_LCD import LCD_Monitor
from helpers.Class_LCD import LCDScrollOptions
from helpers.Class_LCD import LCDinstructions
from helpers.Class_StepMotor import StepMotor
from helpers.Class_ServoMotor import ServoMotor


import helpers.Timers
from subprocess import check_output
import enum


class LCDModes(enum.Enum):
    IPMode = 0
    InfoMode = 1
    LastActionMode = 2
    NetworkMode = 3


class MedicationHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.__timedFuncTouchSensor = TimedFunction(0.2)
        self.__touch = TouchSensor(16)
        self.__kPad = Keypad(6, 13, 19, 26, 0x20, 0, 1, 2, 3)
        self.__timedFuncRFID = TimedFunction(0.2, 1)

        self.__rfidReader = TagReader()

        self.__servoMotor = ServoMotor(18)
        # region LCD
        self.__LCD = LCD_Monitor(24, 23, formatSettings=0b0)
        self.__LCD.SetScrollOption(1, LCDScrollOptions.Right.value |
                                   LCDScrollOptions.EnabledWhenLarge.value)
        self.__LCD.SetScrollOption(0, LCDScrollOptions.Right.value |
                                   LCDScrollOptions.EnabledWhenLarge.value)
        self.__LCD.SetScrollSpacing(0, 2)
        self.__LCD.SetScrollSpacing(1, 2)
        self.__LCD.WriteMessage("Booting ", 0, False)
        self.__LCD.WriteMessage("Booting ", 1)
        self.__LCD.SetScrollSpeed(0, 0.6)
        self.__LCD.SetScrollSpeed(1, 0.6)
        self.__LCD.RewriteMessage("  ", 0)
        self.__LCD.RewriteMessage("  ", 1)
        # endregion LCD

        self.__lcdMode = LCDModes.InfoMode
        self.__lastAction = "No action yet"
        self.__lastInfo = "No info yet"
        self.__lastNetworkInfo = "No networkinfo yet"
        self.ChangeLCDMode(LCDModes.InfoMode)

        self.StepMotor = StepMotor(addressPCF=0x20)

        self.__lampPin = 21
        self.__buzzerPin = 20
        GPIO.setup(self.__lampPin, GPIO.OUT)
        GPIO.setup(self.__buzzerPin, GPIO.OUT)
        self.__dosisReady = False

        self.__scannedCallback = None
        self.__rfidCallbackId = False

        self.__nextMedication = None

        self.__idDrop = None

        # self.__masterBadgeId = 701808313545
        self.__masterBadgeId = 496339390928
        self.__shutdownCode = 4526
        self.__masterCode = 7295

        self.__stepmotortestCode = 4561
        self.__servomotortestCodeOn = 4562
        self.__servomotortestCodeOff = 4563

        GPIO.output(self.__lampPin, False)
        GPIO.output(self.__buzzerPin, False)
        self.__buzzerOn = False

        self.__dataUpdateCallback = None
        self.__shutdown = None

    def __del__(self):
        # self.__LCD.SendInstruction(LCDinstructions.clearDisplay.value)
        self.__LCD.SendInstruction(LCDinstructions.displayOff.value)

        GPIO.output(self.__lampPin, False)
        GPIO.output(self.__buzzerPin, False)
        GPIO.cleanup()

    def update(self):
        self.__LCD.UpdateDisplay()
        self.__HandleKeyPad()
        self.__timedFuncTouchSensor(self.__HandleTouchSensor)
        self.__timedFuncRFID(self.__HandleReader)
        self.HandleNextMedication()

    def __HandleTouchSensor(self):
        # print(f"touch: {self.__touch.CheckState()}")
        if (self.__touch.CheckJustPressed()):
            print(DataRepository.GetNextScheduledMedication())
            DataRepository.LogComponents(3, 1)
            self.LogAction("Touch sensor", "just pressed")
            if ((self.__idDrop == None) or (self.__idDrop == '')):
                self.DepositeMedication()
            pass

    def __HandleKeyPad(self):
        kpValue = self.__kPad.Handle()
        if kpValue == 1:
            code = self.__kPad.Code()
            DataRepository.LogComponents(4, int(code))
            print(code)
            self.__kPad.ResetCode()
            login = DataRepository.LoginAny(code)
            print(login)
            if login == None:
                DataRepository.LogComponents(4, -1)
            else:
                DataRepository.LogComponents(4, login)
            pass
            self.CheckCodes(code)

        if kpValue >= 10:
            if kpValue == 13:
                self.ChangeLCDMode(LCDModes.IPMode)
            elif kpValue == 10:
                self.ChangeLCDMode(LCDModes.InfoMode)
            elif kpValue == 11:
                self.ChangeLCDMode(LCDModes.NetworkMode)
            elif kpValue == 12:
                self.ChangeLCDMode(LCDModes.LastActionMode)

    def __HandleReader(self):
        # print("read")
        self.__ReadRFID()
        # self.__timeOutFuncRFID(self.__ReadRFID)

    def __ReadRFID(self):
        if self.__rfidReader.Read():
            id = self.__rfidReader.getId()
            print(id)
            self.LogAction("Id scanned", id)
            if (int(self.__masterBadgeId) == id):
                print("masterbadge used")
                self.LogAction("masterbadge", "used")
                self.DepositeMedication()
            elif (self.__idDrop != None):
                if (self.__idDrop != ''):
                    print(self.__idDrop)
                    DataRepository.LogComponents(6, id)
                    if (int(self.__idDrop) == id):

                        self.DepositeMedication()
                    else:
                        print(
                            f"{type(int(self.__idDrop))} isn't the same as {type(id)}")

            if (self.__rfidCallbackId and (self.__scannedCallback != None)):
                self.__scannedCallback(id, self.__rfidCallbackId)
                self.__rfidCallbackId = None

            # self.__timeOutFuncRFID.Timeout(2)

    def CheckCodes(self, code):
        if code == '':
            return
        if code == str(self.__shutdownCode):
            self.LogInfo("shutdown down")
            self.LogAction("shutdown down", "")
            self.__shutdown()
            pass
        elif code == str(self.__masterCode):
            self.LogInfo("Mastercode used")
            self.DepositeMedication()
            pass
        elif code == str(self.__stepmotortestCode):
            self.LogInfo("Stepmotor test used")
            self.TurnMotor()
        elif code == str(self.__servomotortestCodeOn):
            self.LogInfo("servo on")
            self.ServoMotor(1)
        elif code == str(self.__servomotortestCodeOff):
            self.LogInfo("servo off")
            self.ServoMotor(0)

    def TurnMotor(self):
        self.LogAction("stepmotor", 4080)
        DataRepository.LogComponents(2, 4080)
        self.StepMotor.turnFull()

    def ServoMotor(self, on):
        if (on):
            self.LogAction("servo", 1)
            DataRepository.LogComponents(1, 1)
            self.__servoMotor.set_angle(90)
        else:
            self.LogAction("servo", 0)
            DataRepository.LogComponents(1, 0)
            self.__servoMotor.set_angle(0)

    def SetScanReturn(self, callback):
        self.__scannedCallback = callback

    def SetDataUpdateReturn(self, callback):
        self.__dataUpdateCallback = callback

    def SetShutdown(self, callback):
        self.__shutdown = callback

    def SetScanReturnId(self, id):
        self.__rfidReader.reset()
        self.__rfidCallbackId = id

    def HandleNextMedication(self):
        if (self.__nextMedication == None):
            self.__nextMedication = DataRepository.GetNextScheduledMedication()
            self.LogInfo(f"{self.__nextMedication['Name']} is next")
        elif (self.__dosisReady):
            GPIO.output(self.__lampPin, True)
            if (self.__buzzerOn):
                GPIO.output(self.__buzzerPin, True)
        elif (self.__nextMedication["Time"].timestamp() < time.time()):
            self.LogAction("New dosis", "ready")
            self.LogInfo(f"{self.__nextMedication['Name']} is now")
            self.__dosisReady = True
            DataRepository.SetNextDropActive()
            print("new dosis ready")
            self.__nextMedication = DataRepository.GetNextScheduledMedication()
            self.__idDrop = self.__nextMedication["RFID"]
            self.LogAction("RFID needed", self.__idDrop)
            print(self.__nextMedication)
            self.__dataUpdateCallback()
        else:
            GPIO.output(self.__lampPin, False)
            GPIO.output(self.__buzzerPin, False)

    def DepositeMedication(self):
        if (self.__nextMedication["Status"] == "InProgress"):
            # print(delay)
            DataRepository.SetActiveDropTaken(0)
            self.__nextMedication = None
            print("vroom vroom medication being dropped weee")
            self.LogAction("Medication dropped", "started")
            self.TurnMotor()
            self.LogAction("Medication dropped", "successfull")
            self.__dataUpdateCallback()
            self.__dosisReady = False
            self.__idDrop = None

    def RecheckMedication(self):
        self.__dosisReady = False
        self.__idDrop = None
        self.__nextMedication = None

    def ChangeLCDMode(self, newMode):
        if (newMode == LCDModes.IPMode):
            ipaddresses = check_output(
                ['hostname', '--all-ip-addresses']).decode('utf-8')
            ipaddresses = ipaddresses[0:len(ipaddresses)-2]
            self.__LCD.RewriteMessage("Ip addresses:", 0, False)
            self.__LCD.RewriteMessage(ipaddresses, 1)
            self.__lcdMode = LCDModes.IPMode
        if (newMode == LCDModes.InfoMode):
            self.__lcdMode = LCDModes.InfoMode
            self.__LCD.DoubleWrite(self.__lastInfo, "")
            pass
        if (newMode == LCDModes.LastActionMode):
            self.__lcdMode = LCDModes.LastActionMode
            self.__LCD.DoubleWrite(self.__lastAction, "")
            pass
        if (newMode == LCDModes.NetworkMode):
            self.__lcdMode = LCDModes.NetworkMode
            self.__LCD.DoubleWrite(self.__lastNetworkInfo, "")
            pass

    def LogAction(self, action, result):
        newAction = f"{action}: {result}"
        if (self.__lcdMode == LCDModes.LastActionMode):
            self.__LCD.DoubleWrite(f" {self.__lastAction}", f" {newAction}")
        self.__lastAction = newAction

    def LogInfo(self, info):
        if (self.__lcdMode == LCDModes.InfoMode):
            self.__LCD.DoubleWrite(f" {self.__lastInfo}", f" {info}")
        self.__lastInfo = info

    def LogNetwork(self, networkinfo):
        if (self.__lcdMode == LCDModes.NetworkMode):
            self.__LCD.DoubleWrite(
                f" {self.__lastNetworkInfo}", f" {networkinfo}")
        self.__lastNetworkInfo = networkinfo
