import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

#from scan import test
import cv2
from pyzbar.pyzbar import decode
import numpy as np


class MainWidget(Widget):
    pass

class MainApp(App):
    def build(self):
        self.img1 = Image()
        self.img1.fit_mode = 'cover'
        self.img1.size = self.img1.width, 640
        camera = FloatLayout(size = (480,640))
        camera.add_widget(self.img1, len(camera.children))
        self.button1 = Button(
            text = 'a',
            size_hint= (.25,.15),
            valign = 'center',x = '120',
            )
        camera.add_widget(self.button1,0)
        
        

        self.capture = cv2.VideoCapture(0)
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)
        return camera
    def update(self,*args):
        ret,frame = self.capture.read()
        for code in decode(frame):
            pts = np.array([code.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(0,255,255),3)
            #print(code)
            
        #cv2.imshow('CV2 Image',frame)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 

        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1

        def read():
            data=code.data.decode('utf-8')
            return data

        self.button1.bind(
            on_press = print(read())
        )
        
        




if __name__ == '__main__':
    MainApp().run()
    cv2.destroyAllWindows()