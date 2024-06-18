import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior

from check import logTime




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


class MainApp(App):
    def build(self):
        self.img1 = Image()
        self.img1.fit_mode = 'cover'
        self.img1.size = self.img1.width, 640

        self.reader = FloatLayout()
        self.reader.add_widget(self.img1)

        

        camera1 = ScreenManager()
        self.camera1 = camera1
        
        def Switch(instance,*args):

            state = ''
            match instance.source:
                case 'source\Log.png':
                    state = 'Log'
                case 'source\camera.png':
                    state = 'camera'

            self.camera1.current = state
            transition = ""
            if state == 'Log':
                transition = 'up'
            else:
                transition = 'down'
            self.camera1.transition.direction = transition
            return Switch

        self.S2 = Screen(name = 'Log')
        logScreen = AnchorLayout(anchor_x = 'left', anchor_y='bottom')
        log = Label(text = self.logs())
        logScreen.add_widget(CamButton(size_hint = (.15,.15), on_press = Switch))
        logScreen.add_widget(log)
        self.S2.add_widget(logScreen)
            
        
        
        camera1.add_widget(self.S2)
        self.reader.add_widget(LogButton(size_hint = (.15,.15),on_press = Switch))
        self.S1 = Screen(name = 'camera')
        self.S1.add_widget(self.reader)
        camera1.add_widget(self.S1)
        camera1.current = 'camera'
        
        

        self.capture = cv2.VideoCapture(0)
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)
        Clock.schedule_interval(self.read, 1)
        Clock.schedule_interval(self.logs, 1.0/33.0)

        #Only for emergency situation

        # self.button1 = Label(
        #     text = log,
        #     )
        # self.button1.bind(on_press = self.read)
        # camera.add_widget(self.button1)
        
        return camera1
    def update(self,*args):
        ret,frame = self.capture.read()
        for code in decode(frame):
            pts = np.array([code.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(0,255,255),3)
        #     self.code = code
            #print(self.code)
            
        #cv2.imshow('CV2 Image',frame)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 

        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1


    def read(self, *args):
        status = f'{logTime().hour}:{logTime().min}   {logTime().state}'
        file = open('shit.txt','a',encoding='utf-8')
        ret,frame = self.capture.read()
        for code in decode(frame):
            # pts = np.array([code.polygon],np.int32)
            # pts = pts.reshape((-1,1,2))
            # cv2.polylines(frame,[pts],True,(0,255,255),3)
            #print(self.code)
            self.data = code.data.decode('utf-8')
            print(self.data)
            file.writelines(f'{str(self.data)} {status} \n')
            file.close()
    def logs(self,*args):
        filein = open('shit.txt','r',encoding='utf-8')
        res = filein.read()
        filein.close()
        return res
        


        
    
    
    
    
        
    
if __name__ == '__main__':
    MainApp().run()
    cv2.destroyAllWindows()