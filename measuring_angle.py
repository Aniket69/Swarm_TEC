#!usr/bin/env/python34
#OpenCv 3.1.0
#Date 21st July, 2016
#Discription : Measuring angle


import cv2
import numpy as np
import math

# create video capture
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 640
width  = 480

fourcc = cv2.VideoWriter_fourcc('M','J','P','G') #This code capture from a Camera, flip every frame in vertical direction and saves it.
writer = cv2.VideoWriter("angle_tracking.avi", fourcc, 12, (640, 480), True) #returns a bool (True/False)
while True:
    
    # read the frames
    _, frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(3, 3)) #Filter used to reduce the niose

    # convert to hsv and find range of blue colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Conversion of image

    #blue
    thresh = cv2.inRange(hsv, np.array((110, 50, 50)), np.array((130, 255, 255))) #The cv2.inRange  function expects three arguments:
                                                                                    #the first is the image  were we are going to perform color detection,
                                                                                    #the second is the lower  limit of the color you want to detect, and
                                                                                    #the third argument is the upper  limit of the color you want to detect.
    thresh2 = thresh.copy()

    # find contours in the threshold image for blue
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.putText(frame, str(cx) + "," + str(cy), (cx, cy + 20), font, 1,(255,255,0), 2, cv2.LINE_AA) #Draw the text for blue
    cv2.circle(frame,(cx, cy), 2,(0, 255, 0), 20)
    cv2.line(frame,(cx, cy),((height, width)[0], cy),(0, 255, 0), 1, cv2.LINE_AA)

    #red
    thresh3 = cv2.inRange(hsv, np.array((0, 150, 0)), np.array((5, 255, 255)))
    thresh4 = thresh3.copy()

    # find contours in the threshold image for red
    _, contours4,hierarchy = cv2.findContours(thresh3, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area2 = 0
    for cnt in contours4:
        area2 = cv2.contourArea(cnt)
        if area2 > max_area2:
            max_area2 = area2
            best_cnt2 = cnt

    # finding centroids of best_cnt and draw a circle there
    M2 = cv2.moments(best_cnt2)
    cx2,cy2 = int(M2['m10'] / M2['m00']), int(M2['m01'] / M2['m00'])
    cv2.putText(frame, str(cx2) + "," + str(cy2), (cx2, cy2 + 20), font, 1,(255, 255,0), 2, cv2.LINE_AA) #Draw the text for red
    cv2.circle(frame,(cx2, cy2), 2, (0, 255, 0), 20)  
    cv2.line(frame,(cx, cy), (cx2, cy2),(0, 255, 0), 1, cv2.LINE_AA)


    #green
    thresh5 = cv2.inRange(hsv, np.array((130, 0, 130)), np.array((255, 255, 255)))
    thresh6 = thresh5.copy()

    # find contours in the threshold image for red
    _, contours5,hierarchy = cv2.findContours(thresh5, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area3 = 0
    for cnt in contours5:
        area3 = cv2.contourArea(cnt)
        if area3 > max_area3:
            max_area3 = area
            best_cnt3 = cnt

    # finding centroids of best_cnt and draw a circle there
    M3 = cv2.moments(best_cnt3)
    cx3, cy3 = int(M3['m10'] / M3['m00']), int(M3['m01'] / M3['m00'])
    cv2.putText(frame, str(cx3) + "," + str(cy3), (cx3, cy3 + 20), font, 1,(255, 0,255), 2, cv2.LINE_AA) #Draw the text for green
    cv2.circle(frame,(cx3, cy3), 2, (0, 255, 0), 20)  
    cv2.line(frame,(cx2, cy2), (cx3, cy3),(0, 255, 0), 1, cv2.LINE_AA)


    
    #put text angle between blue and red
    cx = float(cx)
    cy = float(cy)
    cx2 = float(cx2)
    cy2 = float(cy2)
    cx3 = float(cx3)
    cy3 = float(cy3)
    angle = int(math.atan2((cy - cy2), (cx2 - cx)) * 180 // math.pi)
    cv2.putText(frame, str(angle),(int(cx2) - 10, (int(cy2) + int(cy) + 50) // 2), font, 1, (255, 255, 0), 2, cv2.LINE_AA) 
    angle2 = int(math.atan2((cy2 - cy3), (cx3 - cx2)) * 180 // math.pi)
    cv2.putText(frame, str(angle2),(int(cx3) - 10, (int(cy3) + int(cy2) + 50) // 2), font, 1, (255, 255, 0), 2, cv2.LINE_AA) 

    #saving video 
    writer.write(frame)
    
    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('Measuring Angle', frame)
    #cv2.imshow('thresh',thresh2)
    
    c = cv2.waitKey(1) % 0x100
    if c == 27 or c == 10:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
