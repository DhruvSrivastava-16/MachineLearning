# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:45:08 2020

@author: DHRUV
"""

# Step0-2 Start Capturing the Video, Reading a video from webcam frame by frame and Detect Faces/Bounding Box:

# Step3 store the largest face and store in the numpy array
import numpy as np

import cv2
#initiate the camera
cap = cv2.VideoCapture(0)

#face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

skip = 0 
face_data = []
filename = input("Enter the name: ")

while True:
    ret,frame = cap.read()          
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    if ret==False:
        continue
    
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)#its going to return the coordinates of the face(s) #1.3 is scale factor and 5 is the neighbour size 
  #  cv2.imshow('Gray Frame',gray_frame)
    faces = sorted(faces, key = lambda f: f[2]*f[3]) #to sort in terms of face size
    print(faces)
        
    for face in faces[-1:]: #picking the last face since its largest in terms of size (area) -- w and h ~ f2 and f3
        x,y,w,h = face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        
      # Extract region of interest and store it:
        offset = 10
        face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
        face_section = cv2.resize(face_section,(100,100))
        
        skip+=1
        if(skip%10): #store every 10th face
            face_data.append(face_section)
            print(len(face_data))
        
        
    cv2.imshow('Video Frame',frame)
    cv2.imshow('Face Section',face_section)


    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break
    
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))    
np.save(filename+'.npy',face_data)
print('Data Saved!')
cap.release()
cv2.destroyAllWindows()



