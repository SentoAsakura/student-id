import cv2
from pyzbar.pyzbar import decode
import numpy as np

#fo = open('shit.txt','a')

class Reader:
    def __init__(self):
        self.data
    
    def read(self):
        cam = cv2.VideoCapture(0)
        while True:
            ret,frame = cam.read()
            for code in decode(frame):
                pts = np.array([code.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(0,255,255),3)
                #print(code)
            
            cv2.imshow('frame',frame)

            key = cv2.waitKey(1)
            fo = open('shit.txt','a')
            
            if key == 13:
                data=code.data.decode('utf-8')
                self.data = str(data)
                fo.writelines(str(data)+'\n')
                fo.close()
            if key==113:
                break
        cam.release()
        cv2.destroyAllWindows()



