import time


class Timer:
    def __init__(self, maxtime: int):
        self.maxtime = maxtime
        self.timer = 0

    def Update(self, deltaTime, autoreset=True):
        self.timer += deltaTime
        if (self.timer > self.maxtime):
            if (autoreset):
                self.timer -= self.maxtime
            return True
        return False

    def SetMax(self, newmax):
        self.maxtime = newmax

    def SetMaxSec(self, newmax):
        self.maxtime = newmax*1000000000

    def Reset(self, fullreset=False):
        if (fullreset):
            self.timer = 0
        else:
            self.timer %= self.maxtime


class ChronoTimer:
    def __init__(self):
        self.lastTime = time.time_ns()

    def Loop(self):
        deltatime = time.time_ns() - self.lastTime
        self.lastTime = time.time_ns()
        return deltatime

    def GetElapsedTime(self):
        return time.time_ns() - self.lastTime
