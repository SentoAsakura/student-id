import cv2
from pyzbar.pyzbar import decode
import numpy as np

cam = cv2.VideoCapture(0)
while True:
    ret,frame = cam.read()
    for code in decode(frame):
        pts = np.array([code.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(0,255,255),3)
    
    cv2.imshow('frame',frame)

    key = cv2.waitKey(1)
    
    if key == 'a':
        data=code.data.decode('utf-8')
        print('A:',data)
    if key==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()