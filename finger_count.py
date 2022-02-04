import cv2
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

path = "fingers"
myList = os.listdir(path)
tipIds = [4, 8, 12, 16, 20]

overlayList = []
for imagePath in myList:
    image = cv2.imread(f'{path}/{imagePath}')
    overlayList.append(image)

detector = htm.HandDetector(detectionCon = 0.7, maxHands = 1)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)

    detector.findHands(image)
    lnList, bBox = detector.findPosition(image, draw = False)

    if len(lnList) != 0:
        totalFingers = detector.fingersUp().count(1)

        h, w, c = overlayList[totalFingers - 1].shape
        image[0:h, 0:w] = overlayList[totalFingers - 1]

    cv2.imshow('Finger count', image)
    if cv2.waitKey(1) == 27:
        break