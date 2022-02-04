import cv2
import HandTrackingModule as htm
import autopy
import pyautogui
import numpy as np
import math

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

wScr, hScr = autopy.screen.size()
frameR = 50

smoothning = 3
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0

detector = htm.HandDetector(detectionCon=0.8, maxHands=1)
scroll_allowed = True

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    
    image = detector.findHands(image)
    lnList, bBox = detector.findPosition(image, draw=False)

    if len(lnList) != 0:
        x1, y1 = lnList[8][1], lnList[8][2]
        x2, y2 = lnList[4][1], lnList[4][2]

        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR - 75), (0, hScr))

        cLocX = pLocX + (x3 - pLocX) / smoothning
        cLocY = pLocY + (y3 - pLocY) / smoothning

        cv2.rectangle(image, (frameR, frameR), (wCam - frameR, hCam - frameR - 75), (0, 255, 0), 2)

        fingers = detector.fingersUp()
        
        if not fingers[2]:
            autopy.mouse.move(cLocX, cLocY)
            pLocX, pLocY = cLocX, cLocY
        if fingers[2] and fingers[1] and x2 >= x1:
            autopy.mouse.click()
        if fingers[0] and fingers[1] and fingers[4] and not fingers[2] and not fingers[3]:
            if scroll_allowed:
                autopy.mouse.click(autopy.mouse.Button.MIDDLE)
            else:
                scroll_allowed = True
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            cv2.destroyAllWindows()
            break

    cv2.imshow("Finger tracking", image)
    
    if cv2.waitKey(1) == 27:
        break
