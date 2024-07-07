import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior

from check import logTime
import dataManage as data




Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

#from scan import test
import cv2
from pyzbar.pyzbar import decode
import numpy as np

class LogButton(ButtonBehavior,Image):
    def __init__(self, **kwargs):
        super(LogButton,self).__init__(**kwargs)
        self.source = 'source\Log.png'
class CamButton(ButtonBehavior,Image):
    def __init__(self, **kwargs):
        super(CamButton,self).__init__(**kwargs)
        self.source = 'source\camera.png'

class LogScreen(Screen):
    def __init__(self, **kw):
        super(LogScreen,self).__init__(**kw)
        logScreen = AnchorLayout(anchor_x = 'left', anchor_y='bottom')

        logScreen.add_widget(CamButton(size_hint = (.15,.15), on_press = self.changeScreen))

        logScreen2 = BoxLayout(orientation='vertical')
        history = Label(text = data.history())
        logScreen2.add_widget(history)
        
        self.add_widget(logScreen)
        self.add_widget(logScreen2)
    def changeScreen(self, *args):
        self.manager.transition.direction = 'down'
        self.manager.current = 'camera'

class Reader(Screen):
    def __init__(self, **kw):
        super(Reader, self).__init__(**kw)
        self.img1 = Image()
        self.img1.fit_mode = 'cover'
        self.img1.size = self.img1.width, 640

        self.reader = FloatLayout()
        self.reader.add_widget(self.img1)

        self.reader.add_widget(LogButton(size_hint = (.15,.15),on_press = self.screenChange))
        self.add_widget(self.reader)

        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0/33.0)
        Clock.schedule_interval(self.read, 1)
    def screenChange(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'log'
    def update(self,*args):
        ret,frame = self.capture.read()
        for code in decode(frame):
            pts = np.array([code.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(0,255,255),3)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 

        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1


    def read(self, *args):
        ret,frame = self.capture.read()
        out_data = None
        for code in decode(frame):
            self.data = code.data.decode('utf-8')
            try:
                out_data = int(self.data)
            except:
                print('An error occured')
            finally:
                if out_data != None:
                    data.find_n_update(out_data)
            print(self.data)



class MainApp(App):
    def build(self):
        camera1 = ScreenManager()
        self.S2 = LogScreen(name = 'log')
        camera1.add_widget(self.S2)
        self.S1 = Reader(name = 'camera')
        camera1.add_widget(self.S1)
        camera1.current = 'camera'
        return camera1
            
    def logs(self,*args):
        filein = open('log.txt','r',encoding='utf-8')
        res = filein.read()
        filein.close()
        return res
        


        
    
    
    
    
        
    
if __name__ == '__main__':
    MainApp().run()
    cv2.destroyAllWindows()