import cv2
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon = 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    
    image = detector.findHands(image)
    lnList = detector.findPosition(image, draw = False)
    
    if len(lnList) != 0:

        

        x1, y1 = lnList[4][1], lnList[4][2] 
        x2, y2 = lnList[8][1], lnList[8][2] 
        cv2.circle(image, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 4)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        if length <= 20:
            cv2.circle(image, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        
        vol = np.interp(length, [15, 210], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        
        

    cv2.imshow("Finger tracking", image)
    
    if cv2.waitKey(1) == 27:
        break