import time
import json
setting = json.load(open('setting.json'))

mode1 = setting["mode1"]
mode2 = setting["mode2"]
class logTime():
    def __init__(self):
        self.time = time.localtime()
        self.hour = self.time.tm_hour
        self.min = self.time.tm_min
        self.state = self.check(setting["mode"])
    def check(self, mode):
        match mode:
            case '1':
                if self.hour == mode1[0] and self.min>mode1[1]:
                    return 'Trễ'
                elif self.hour >= mode1[2]:
                    return 'Trễ'
                else: return 'Đúng giờ'
            case '2':
                if self.hour == mode2[0] and self.min>mode2[1]:
                    return 'Trễ'
                elif self.hour >= mode2[2]:
                    return 'Trễ'
                else: return 'Đúng giờ'