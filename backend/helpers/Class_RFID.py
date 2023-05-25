import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class TagReader:
    def __init__(self):
        self.__reader = SimpleMFRC522()
        self.__id = None
        self.__text = None

    def Read(self):
        if self.__id == None:
            self.__id, self.__text = self.__reader.read_no_block()
            if self.__id != None:
                return True
        return False
            
    
    def getId(self):
        return self.__id
    
    def reset(self):
        self.__id = None
        self.__text = None