import numpy as np
import cv2
import time

face_cascade = cv2.CascadeClassifier('classifiers/face/haarcascade_frontalface_default.xml')
#car_cascade = cv2.CascadeClassifier('classifiers/classifier/cascade.xml')
#car_cascade = cv2.CascadeClassifier('classifiers/cars/haarcascade_car_1.xml')
#prof_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_profileface.xml')
#eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    ret,img = cap.read()
    #img = cv2.imread('classifiers\cars\test\test0000.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('output', gray)

    #face marking
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    #side_faces = prof_face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    #another type (side) of face detection
    #for (x,y,w,h) in side_faces:
        #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    #car detection
    #cars = car_cascade.detectMultiScale(gray, 1.3, 10)
    #for (x,y,w,h) in cars:
        #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        
    cv2.imshow('Webcam',img)
    time.sleep(0.05)
        
    k=cv2.waitKey(10)
    if k==27:
        break


#cv2.waitKey(0)
cv2.destroyAllWindows()
