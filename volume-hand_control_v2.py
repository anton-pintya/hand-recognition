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

detector = htm.HandDetector(detectionCon = 0.7, maxHands = 1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

area = 0

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    
    image = detector.findHands(image)
    lnList, bBox = detector.findPosition(image, draw = False)
    
    if len(lnList) != 0:
        area = (bBox[2] - bBox[0]) * (bBox[3] - bBox[1]) // 100

        if 100 < area < 1100:
            length, image, lineInfo = detector.findDistance(4, 8, image)
            
            volPer = np.interp(length, [15, 210], [0, 100])

            smoothness = 10
            volPer = smoothness * round(volPer / smoothness)

            fingers = detector.fingersUp()
            
            if not fingers[4] and not fingers[3]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(image, (lineInfo[4], lineInfo[5]), 10, (0, 230, 0), cv2.FILLED)       

    cv2.imshow("Finger tracking", image)
    
    if cv2.waitKey(1) == 27:
        break