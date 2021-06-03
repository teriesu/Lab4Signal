import cv2
import mediapipe as mp
import time
import csv

cap = cv2.VideoCapture(0) ## Web Cam ID

mpHands= mp.solutions.hands

hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

NameCSVAcX = "SamplesCam2\CameraSamples2.csv"
MatAcX = []
line = 0
num_samples = 500

pTime=0
cTime= 0
while line < num_samples:
    success, img = cap.read()

    imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result= hands.process(imgRGB)
    # print(result.multi_hand_landmarks) True if hand is identify

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks: # Extract the information to each hand
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id==8:
                    print(id,cx,cy)
                    cv2.circle(img, (cx,cy),25,(255,0,255),cv2.FILLED)
                    fileAcX = open(NameCSVAcX, "a")
                    fileAcX.write(str(float(cx)) +','+ str(float(cy)) + "\n")

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime= time.time()
    fps= 1/(cTime-pTime)
    pTime=cTime
    cv2.imshow("Output",img)
    line = line + 1
    cv2.waitKey(1)

fileAcX.close()
