import cv2
import numpy as np
import time
import hand_tracking_module as hmt
import math
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

####################################
wCam , hCam = 1000 , 800
####################################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = hmt.handDetector(detectionCon=0.7)
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]




while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4],lmList[8])
        x1,y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1 + x2) // 2 , (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img , (x1, y1),(x2, y2),(0,0,255),2)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)

        vol = np.interp(length, [25, 175], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        print(length)
        if length <= 30:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        elif 30<length<165 :
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        elif length >=165:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,f"FPS:{int(fps)}",(30,30), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)





    if not success :
        print("unable to get ")
        break
    cv2.imshow("vid",img)
    if cv2.waitKey(1) & 0xFF == ord("Q"):
        break