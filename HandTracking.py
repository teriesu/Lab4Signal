import cv2
import mediapipe as mp
import time
import serial
serialPy = serial.Serial("COM4", 9600)
cap = cv2.VideoCapture(0) ## Web Cam ID
mpHands= mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Constantes filtro
b1 = 2.205959670705249e-04
b2 = 6.617879012115746e-04
b3 = 6.617879012115746e-04
b4 = 2.205959670705249e-04
a2 = 2.827126382896457
a3 = -2.685160746458055
a4 = 0.856269595825034
#corrimientos x
Ax_X = 0
Ay_X = 0
Ax_1_X = 0
Ax_2_X = 0
Ax_3_X = 0
Ay_1_X = 0
Ay_2_X =0
Ay_3_X = 0
#corrimientos y
Ax_Y = 0
Ay_Y = 0
Ax_1_Y = 0
Ax_2_Y = 0
Ax_3_Y = 0
Ay_1_Y = 0
Ay_2_Y =0
Ay_3_Y = 0

pTime=0
cTime= 0
while True:
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
                    #print(id,cx,cy)

                    ##################Filtrado IIR################
                    Ax_X = cx
                    Ay_X = b1*Ax_X + b2*Ax_1_X + b3*Ax_2_X + b4*Ax_3_X + a2*Ay_1_X + a3*Ay_2_X + a4*Ay_3_X
                    #Corrimientos de entrada
                    Ax_3_X = Ax_2_X
                    Ax_2_X = Ax_1_X
                    Ax_1_X = Ax_X
                    #Corrimientos de filtro
                    Ay_3_X = Ay_2_X
                    Ay_2_X = Ay_1_X
                    Ay_1_X = Ay_X
                    A_X_fil = int(Ay_X)

                    Ax_Y = cy
                    Ay_Y = b1*Ax_Y + b2*Ax_1_Y + b3*Ax_2_Y + b4*Ax_3_Y + a2*Ay_1_Y + a3*Ay_2_Y + a4*Ay_3_Y
                    #Corrimientos de entrada
                    Ax_3_Y = Ax_2_Y
                    Ax_2_Y = Ax_1_Y
                    Ax_1_Y = Ax_Y
                    #Corrimientos de filtro
                    Ay_3_Y = Ay_2_Y
                    Ay_2_Y = Ay_1_Y
                    Ay_1_Y = Ay_Y
                    A_Y_fil = int(Ay_Y)

                    cadena = str(A_X_fil) + ',' + str(A_Y_fil) + '\n'
                    serialPy.write(bytes(cadena, 'utf-8'))
                    print(bytes(cadena, 'utf-8'))
                    cv2.circle(img, (cx,cy),25,(255,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime= time.time()
    fps= 1/(cTime-pTime)
    pTime=cTime
    cv2.imshow("Output",img)
    cv2.waitKey(1)
    #line = (arduino.readline().decode('utf-8'))
    #print(chr(int(line)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        serialPy.close()
        break
