import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # The color space is BGR by default.
    # Other options include HSV, 

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set the filter's color bounds
    lower_red = np.array([0,0,50])
    upper_red = np.array([255,255,255])

    # Mask is black and white (0 or 1) which pixels fall in range
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Smooth out the high frequency noise
    # Options: averaging, gaussian blurring, median blur, bilateral blur
    median = cv2.medianBlur(res,15)
    cv2.imshow('Median Blur',median)
    cv2.imshow('frame',frame)
    # Display the resulting frame
    # cv2.imshow('WINDOW_TITLE', FRAME_VARIABLE)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
    #if k == ord('d'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

##import cv2
##import numpy as np
##
##def nothing(x):
##    pass
##
### Create a black image, a window
##img = np.zeros((300,512,3), np.uint8)
##cv2.namedWindow('image')
##
### create trackbars for color change
##cv2.createTrackbar('R','image',0,255,nothing)
##cv2.createTrackbar('G','image',0,255,nothing)
##cv2.createTrackbar('B','image',0,255,nothing)
##
### create switch for ON/OFF functionality
##switch = '0 : OFF \n1 : ON'
##cv2.createTrackbar(switch, 'image',0,1,nothing)
##
##while(1):
##    cv2.imshow('image',img)
##    k = cv2.waitKey(1) & 0xFF
##    if k == 27:
##        break
##
##    # get current positions of four trackbars
##    r = cv2.getTrackbarPos('R','image')
##    g = cv2.getTrackbarPos('G','image')
##    b = cv2.getTrackbarPos('B','image')
##    s = cv2.getTrackbarPos(switch,'image')
##
##    if s == 0:
##        img[:] = 0
##    else:
##        img[:] = [b,g,r]
##
##cv2.destroyAllWindows()
