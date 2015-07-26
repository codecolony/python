import numpy as np
import cv2
import time

#face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
#car_cascade = cv2.CascadeClassifier('classifiers/classifier/cascade.xml')
car_cascade = cv2.CascadeClassifier('classifiers/cars/haarcascade_car_1.xml')
#prof_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_profileface.xml')
#eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')

img = cv2.imread('classifiers/cars/test/test0001.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#car detection
cars = car_cascade.detectMultiScale(gray, 1.1, 3)
for (x,y,w,h) in cars:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        
cv2.imshow('Loaded Image',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
