import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('videoEntrada.mp4')
bg = None

#COLORES PARA LA VISUALIOZACIÓN
color_start = (204, 204, 0)
color_end = (240, 0, 204)
color_far = (255, 0, 0)

color_start_far = (204, 204, 0)
color_far_end = (204, 0, 204)
color_start_end = (0, 255, 255)

color_contorno = (0, 255, 0)
color_ymin = (0, 130, 255) #Punto mas alto del contorno
color_angulo = (0, 255, 255)
color_d = (0, 255, 255)
color_fingers = (0, 255, 255)

while cap.isOpened():
    ret, frame = cap.read()
    if ret == False: break

    frame = imutils.resize(frame, width = 640) #Tamaño del Frame
    frame = cv2.flip(frame, 1) #Espejo
    frameAux = frame.copy()

    if bg is not None:
        cv2.imshow('bg', bg)

    cv2.imshow('Frame', frame)

    k = cv2.waitKey(1)
    if k == ord('i'):
        bg = cv2.cvtColor(frameAux, cv2.COLOR_RGB2GRAY) #Almancenamos el fondo de la imágen
        cv2.imwrite('cali11.png', frameAux)
    if k == ord('q'):
       	break

cap.release()
cv2.destroyAllWindows()

#Prueba
