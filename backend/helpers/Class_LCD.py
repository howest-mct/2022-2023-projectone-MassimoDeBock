from RPi import GPIO
import time
import enum

from helpers.Timers import Timer
from helpers.Timers import ChronoTimer
from helpers.Class_PCF import PCF

# i used https://fsymbols.com/generators/tarty/ for these big texts

# ─────────────────────────────────────────────────────────────────────────────
# ─██████████████─██████──────────██████─██████──██████─██████──────────██████─
# ─██░░░░░░░░░░██─██░░██████████──██░░██─██░░██──██░░██─██░░██████████████░░██─
# ─██░░██████████─██░░░░░░░░░░██──██░░██─██░░██──██░░██─██░░░░░░░░░░░░░░░░░░██─
# ─██░░██─────────██░░██████░░██──██░░██─██░░██──██░░██─██░░██████░░██████░░██─
# ─██░░██████████─██░░██──██░░██──██░░██─██░░██──██░░██─██░░██──██░░██──██░░██─
# ─██░░░░░░░░░░██─██░░██──██░░██──██░░██─██░░██──██░░██─██░░██──██░░██──██░░██─
# ─██░░██████████─██░░██──██░░██──██░░██─██░░██──██░░██─██░░██──██████──██░░██─
# ─██░░██─────────██░░██──██░░██████░░██─██░░██──██░░██─██░░██──────────██░░██─
# ─██░░██████████─██░░██──██░░░░░░░░░░██─██░░██████░░██─██░░██──────────██░░██─
# ─██░░░░░░░░░░██─██░░██──██████████░░██─██░░░░░░░░░░██─██░░██──────────██░░██─
# ─██████████████─██████──────────██████─██████████████─██████──────────██████─
# ─────────────────────────────────────────────────────────────────────────────


class LCDinstructions(enum.Enum):
    clearDisplay = 0b00000001
    cursorHome = 0b00000010
    displayOff = 0b00001000
    displayOnWCursor = 0b00001111
    functionSet = 0b00111000
    setDDRAM = 0b10000000

    displayShiftL = 0b00011000
    displayShiftR = 0b00011100
    displayReturnHome = 0b00000010

    setDDRAMLine0 = 0b10000000
    setDDRAMLine1 = 0b11000000


class LCDFormatting(enum.Enum):
    wrap = 0b00000001


class LCDDisplayOptions(enum.Enum):
    autoscroll0L = 0b00000001
    autoscroll0R = 0b00000010
    autoscroll1L = 0b00000100
    autoscroll1R = 0b00001000
    autoscrollFL = 0b00000101
    autoscrollFR = 0b00001010


class LCDScrollOptions(enum.Enum):
    Enabled = 0b10000000
    EnabledWhenLarge = 0b01000000
    Left = 0b00000001
    Right = 0b00000000
    Repeat = 0b00000010


# ─────────────────────────────────────────────────────────────
# ─██████████─██████──────────██████─██████████─██████████████─
# ─██░░░░░░██─██░░██████████──██░░██─██░░░░░░██─██░░░░░░░░░░██─
# ─████░░████─██░░░░░░░░░░██──██░░██─████░░████─██████░░██████─
# ───██░░██───██░░██████░░██──██░░██───██░░██───────██░░██─────
# ───██░░██───██░░██──██░░██──██░░██───██░░██───────██░░██─────
# ───██░░██───██░░██──██░░██──██░░██───██░░██───────██░░██─────
# ───██░░██───██░░██──██░░██──██░░██───██░░██───────██░░██─────
# ───██░░██───██░░██──██░░██████░░██───██░░██───────██░░██─────
# ─████░░████─██░░██──██░░░░░░░░░░██─████░░████─────██░░██─────
# ─██░░░░░░██─██░░██──██████████░░██─██░░░░░░██─────██░░██─────
# ─██████████─██████──────────██████─██████████─────██████─────
# ─────────────────────────────────────────────────────────────

class LCD_Monitor:
    def __init__(self, rsPin, pulsePin, screenWidth=16, formatSettings=0b0):
        self.__pcf = PCF(0x24)
        self.__rsPin = rsPin
        self.__pulsePin = pulsePin
        self.__formatSettings = formatSettings
        self.__screenWidth = screenWidth
        self.__maxLines = 2
        self.__hardcapwidth = 64

        self.__chrono = ChronoTimer()

        self.__scrollTimer = [Timer(5), Timer(5)]
        self.__scrollIndex = [0, 0]
        self.__scrollOptions = [0b0, 0b0]
        self.__scrollSpacing = [screenWidth, screenWidth]

        self.__data = ['', '']

        GPIO.setup(self.__rsPin, GPIO.OUT)
        GPIO.setup(self.__pulsePin, GPIO.OUT)
        self.SendInstruction(LCDinstructions.functionSet.value)
        self.SendInstruction(LCDinstructions.displayOnWCursor.value)
        self.SendInstruction(LCDinstructions.clearDisplay.value)

        self.SendInstruction(LCDinstructions.cursorHome.value)
        # GPIO.output()

    def __del__(self):
        # self.SendInstruction(LCDinstructions.clearDisplay.value)
        pass

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─██████──██████─██████████████─██████─────────██████████████─██████████████─████████████████───██████████████─
# ─██░░██──██░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─
# ─██░░██──██░░██─██░░██████████─██░░██─────────██░░██████░░██─██░░██████████─██░░████████░░██───██░░██████████─
# ─██░░██──██░░██─██░░██─────────██░░██─────────██░░██──██░░██─██░░██─────────██░░██────██░░██───██░░██─────────
# ─██░░██████░░██─██░░██████████─██░░██─────────██░░██████░░██─██░░██████████─██░░████████░░██───██░░██████████─
# ─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─
# ─██░░██████░░██─██░░██████████─██░░██─────────██░░██████████─██░░██████████─██░░██████░░████───██████████░░██─
# ─██░░██──██░░██─██░░██─────────██░░██─────────██░░██─────────██░░██─────────██░░██──██░░██─────────────██░░██─
# ─██░░██──██░░██─██░░██████████─██░░██████████─██░░██─────────██░░██████████─██░░██──██░░██████─██████████░░██─
# ─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─██░░██──██░░░░░░██─██░░░░░░░░░░██─
# ─██████──██████─██████████████─██████████████─██████─────────██████████████─██████──██████████─██████████████─
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────

    def __SetInstructionMode(self):
        GPIO.output(self.__rsPin, False)

    def __SetDataMode(self):
        GPIO.output(self.__rsPin, True)

    def __Pulse(self):
        GPIO.output(self.__pulsePin, False)
        time.sleep(0.01)
        GPIO.output(self.__pulsePin, True)

    def __UpdateCurrentData(self, value, line=0):
        self.__data[line] += chr(value)

    def __SendDataBits(self, value):
        self.__pcf.SetSpecificBits(0b11111111, value)
        self.__Pulse()

    def __PadMessage(self, message):
        return message + " "*(self.__screenWidth - len(message))


# ─────────────────────────────────────────────────────────────────────────────────────────
# ─██████████████─██████──██████─██████████████───██████─────────██████████─██████████████─
# ─██░░░░░░░░░░██─██░░██──██░░██─██░░░░░░░░░░██───██░░██─────────██░░░░░░██─██░░░░░░░░░░██─
# ─██░░██████░░██─██░░██──██░░██─██░░██████░░██───██░░██─────────████░░████─██░░██████████─
# ─██░░██──██░░██─██░░██──██░░██─██░░██──██░░██───██░░██───────────██░░██───██░░██─────────
# ─██░░██████░░██─██░░██──██░░██─██░░██████░░████─██░░██───────────██░░██───██░░██─────────
# ─██░░░░░░░░░░██─██░░██──██░░██─██░░░░░░░░░░░░██─██░░██───────────██░░██───██░░██─────────
# ─██░░██████████─██░░██──██░░██─██░░████████░░██─██░░██───────────██░░██───██░░██─────────
# ─██░░██─────────██░░██──██░░██─██░░██────██░░██─██░░██───────────██░░██───██░░██─────────
# ─██░░██─────────██░░██████░░██─██░░████████░░██─██░░██████████─████░░████─██░░██████████─
# ─██░░██─────────██░░░░░░░░░░██─██░░░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░██─██░░░░░░░░░░██─
# ─██████─────────██████████████─████████████████─██████████████─██████████─██████████████─
# ─────────────────────────────────────────────────────────────────────────────────────────


# d) Schrijf de send_instruction(value). Deze methode zet de RS lijn op het correcte niveau en
# maakt een klokpuls met de E lijn. (van hoog naar laag = inlezen). Deze methode roept ook
# de methode set_data_bits(value) aan.


    def SendInstruction(self, value):
        self.__SetInstructionMode()
        self.__SendDataBits(value)

# e) Schrijf de send_character(value). Idem als daarnet maar met de RS lijn op data input.

    def __SendCharacter(self, value, line=0):
        self.__SetDataMode()
        self.__SendDataBits(value)
        # print(self.currentSpot)

    def AddText(self, text, line=0):
        if (self.__formatSettings & LCDFormatting.wrap.value):
            self.__data[0] += text
            return
        self.__data[line] += text

    def ChangeText(self, text, line=0):
        if (self.__formatSettings & LCDFormatting.wrap.value):
            self.__data[0] = text
            return
        self.__data[line] = text

    # i) Schrijf een def write_message(message). Deze methode overloopt het bericht en schrijft
    # karakter per karakter naar het LCD display.

    def __SendMessage(self, message, line=0):
        if (line == 0):
            self.SendInstruction(LCDinstructions.setDDRAMLine0.value)
        else:
            self.SendInstruction(LCDinstructions.setDDRAMLine1.value)
        for char in message:
            self.__SendCharacter(ord(char), line)

    def RewriteMessage(self, message, line=0, rewrite=True):
        self.ChangeText(message, line)
        self.__scrollIndex[line] = 0
        if (rewrite):

            self.RewriteDisplay()

    def WriteMessage(self, message, line=0, rewrite=True):
        self.AddText(message, line)
        if (rewrite):
            self.RewriteDisplay()

    def DoubleWrite(self, message, message2):
        self.ChangeText(message, 0)
        self.ChangeText(message2, 1)
        self.RewriteDisplay()

# j) Vraag een input van de gebruiker. De ingegeven tekst druk je af op het display. Zorg er ook voor dat
# de tekst correct wordt weergeven als de tekst meer dan 16 karakters bedraagt. Los dit op door gebruik
# te maken van een extra instructie tussendoor.

    def PromptInput(self, prompt, line=0, rewrite=True):
        message = input(f'{prompt} ')
        if (rewrite):
            self.RewriteMessage(message, line)
        else:
            self.WriteMessage(message, line)
        return message

    # def update_display(self, delay):
    #     if(self.formatSettings)

    def SetScrollSpeed(self, line, scrollspeed):
        if (line >= 0 and line < len(self.__scrollTimer)):
            self.__scrollTimer[line].SetMaxSec(scrollspeed)

    def SetScrollOption(self, line, scrollOption):
        self.__scrollOptions[line] = scrollOption

    def SetScrollIndex(self, line, displayIndex):
        self.__scrollIndex[line] = displayIndex

    def SetScrollSpacing(self, line, spacing):
        self.__scrollSpacing[line] = spacing


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─████████████───██████████─██████████████─██████████████─██████─────────██████████████─████████──████████─
# ─██░░░░░░░░████─██░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
# ─██░░████░░░░██─████░░████─██░░██████████─██░░██████░░██─██░░██─────────██░░██████░░██─████░░██──██░░████─
# ─██░░██──██░░██───██░░██───██░░██─────────██░░██──██░░██─██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
# ─██░░██──██░░██───██░░██───██░░██████████─██░░██████░░██─██░░██─────────██░░██████░░██───████░░░░░░████───
# ─██░░██──██░░██───██░░██───██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─────████░░████─────
# ─██░░██──██░░██───██░░██───██████████░░██─██░░██████████─██░░██─────────██░░██████░░██───────██░░██───────
# ─██░░██──██░░██───██░░██───────────██░░██─██░░██─────────██░░██─────────██░░██──██░░██───────██░░██───────
# ─██░░████░░░░██─████░░████─██████████░░██─██░░██─────────██░░██████████─██░░██──██░░██───────██░░██───────
# ─██░░░░░░░░████─██░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─██░░██──██░░██───────██░░██───────
# ─████████████───██████████─██████████████─██████─────────██████████████─██████──██████───────██████───────
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────

    def RewriteDisplay(self):
        if (self.__formatSettings & LCDFormatting.wrap.value):
            self.__SendMessage(self.__data[0][0:self.__screenWidth], 0)
            self.__SendMessage(
                self.__data[0][self.__screenWidth:self.__screenWidth*2], 1)
        else:
            for i in range(self.__maxLines):
                self.__SendMessage(self.__PadMessage(
                    self.__GetDisplayText(i)), i)

    def UpdateDisplay(self):
        shouldUpdate = False
        deltaTime = self.__chrono.Loop()
        for line in range(self.__maxLines):
            if (bool(self.__scrollOptions[line] & LCDScrollOptions.Enabled.value) |
                    (bool(self.__scrollOptions[line] & LCDScrollOptions.EnabledWhenLarge.value) & bool(len(self.__data[line]) > self.__screenWidth))):
                shouldUpdate = shouldUpdate | self.__ScrollLine(
                    line, deltaTime, self.__scrollOptions[line] & LCDScrollOptions.Left.value)
        if (shouldUpdate):
            self.RewriteDisplay()


# scoll


    def __ScrollLine(self, line, deltaTime, scrollLeft=True):
        if (self.__scrollTimer[line].Update(deltaTime)):
            if (scrollLeft):
                if (self.__scrollIndex[line] <= 0):
                    self.__scrollIndex[line] = len(
                        self.__data[line]) + self.__scrollSpacing[line]-1
                else:
                    self.__scrollIndex[line] -= 1
            else:
                self.__scrollIndex[line] += 1
                self.__scrollIndex[line] %= len(
                    self.__data[line]) + self.__scrollSpacing[line]
            return True
        return False

    def __GetDisplayText(self, line):
        tempText = ""
        index = self.__scrollIndex[line]

        if (len(self.__data[line]) <= 0):
            return ""
        if (len(self.__data[line]) <= self.__screenWidth):
            return self.__data[line]
        if (index < 0):
            return self.__data[line]
        while len(tempText) < self.__screenWidth:
            currentIndex = (
                index + len(tempText)) % (len(self.__data[line])+self.__scrollSpacing[line])
            if (currentIndex < len(self.__data[line])):
                tempText += self.__data[line][currentIndex:currentIndex +
                                              min(len(self.__data[line]), self.__screenWidth-len(tempText))]
            else:
                tempText += ' '*(min(self.__scrollSpacing[line] - (
                    currentIndex-len(self.__data[line])), self.__screenWidth-len(tempText)))
        # print(f"{tempText} : {index}")
        return tempText
