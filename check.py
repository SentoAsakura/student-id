import time

class logTime():
    def __init__(self):
        self.time = time.localtime()
        self.hour = self.time.tm_hour
        self.min = self.time.tm_min
        self.state = self.check()
    def check(self):
        if self.hour>=7:
            return 'Trễ'
        if self.hour == 6 and self.min>45:
            return 'Trễ'
        else: return 'Đúng giờ'