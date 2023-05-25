import time


class TimeOutableFunction:
    def __init__(self):
        self.__timedOutTill = time.time()

    def __call__(self, call_method):
        if self.__timedOutTill < time.time():
            call_method()

    def Timeout(self, timeout):
        self.__timedOutTill = time.time() + timeout

    
