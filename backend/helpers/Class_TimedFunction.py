import time


class TimedFunction:
    def __init__(self, frequenty, offset=0):
        self.__startTime = offset
        self.__loopDelay = self.__startTime + frequenty

    def executeManaged(self, call_method):
        if self.__startTime < time.time():
            call_method()

            self.__startTime = time.time() + self.__loopDelay

    def __call__(self, call_method):
        if self.__startTime < time.time():
            call_method()

            self.__startTime = time.time() + self.__loopDelay
