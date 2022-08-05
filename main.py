import cv2
import os
import time
import numpy as np
import serial

ard= serial.Serial()
ard.port = "COM3"
ard.baudrate = 9600
ard.open()

cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
cascPatheyes = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_eye_tree_eyeglasses.xml"
#
faceCascade = cv2.CascadeClassifier(cascPathface)
eyeCascade = cv2.CascadeClassifier(cascPatheyes)


video_capture = cv2.VideoCapture(1)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read(0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
        faceROI = frame[y:y+h,x:x+w]
        eyes = eyeCascade.detectMultiScale(faceROI)
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            frame = cv2.circle(frame, eye_center, radius, (255, 0, 0), 4)


        Xpos = x+(w/2)#calculates the X coordinate of the center of the face.
        Ypos = y+(h/2)#calculates the Y coordinate of the center of the face.
    
        print("posisi x =  "+str(Xpos))
        print("posisi y =  "+str(Ypos))

        if Xpos >= 380:
            ard.write('L'.encode())#The following code check if the face is on the left, 
            print("left")
            time.sleep(0.01)        # right, top or botton, 
        elif Xpos <= 260:           #with respect to the center of the frame
            ard.write('R'.encode())#if any conditions are true, it send a commant 
            print("right")
            time.sleep(0.01)       #to the arduino throught the serial bus.    
        

        if Ypos > 300:
            ard.write('D'.encode())
            print("down")
            time.sleep(0.01)
        elif Ypos < 180:
            ard.write('U'.encode())
            print("up")
            time.sleep(0.01)

        break 

    cv2.imshow('Video', frame)# Display the resulting frame
      
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()