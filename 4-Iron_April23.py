## Updated: Apr 23, 2017
## To do:
## Add a cancel button for tests
## Finish debugging progress label for R&D Test
##      Add progress label for USGA Full Map Test
## Add easy-click icon to desktop to run the proram
## Add options button to switch to left-handed club (and all underlying support code)
## Add button + entry-box for arbitrary lie-angles 

import RPi.GPIO as gpio
import time
import sys
import math
import numpy as np
from functools import partial

import tkinter
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import PhotoImage
from tkinter import *

# Variables for easy changes

# Conversion ratios: milimeters -> steps
mm2steps_horiz = 25
mm2steps_vert = 25
mm2steps_pend = 25
steps2mm_horiz = 1/mm2steps_horiz
steps2mm_vert = 1/mm2steps_vert
steps2mm_pend = 1/mm2steps_pend

# Pendulum heights in motor steps
pend_lowHeight = 1000
pend_medHeight = 1900
pend_highHeight = 2750

# Common testing points
toe20 = 26
heel20 = 18
low10 = 4
high10 = 40
toe10high10 = 42
center = 22

# Servo settings
freq_servo = 50 # in Hz
servoPos_dropped = 3
servoPos_grabbed = 5

# GUI sizes and colors
menusize = '800x450-0+0'
buttonwidth = 6
buttonheight = 4
buttonsize_relative = 0.3
gotogrid_offset_x = 55
gotogrid_offset_y = 80

# Logo gold = "#d4bc20"
buttonColor = "#ffd700" # Also gold
bColor_active = "#22bb22" # Forest green
title_top = 'Automated Clubface CT Tester'
title_calibrate = "Positional Calibration"
title_manual = 'Manual Control'
title_goto = 'Go To Point'
title_options = 'Options'

sleeptime = 2/1000 # In seconds

# RPi physical pins
pin_stepHorizontal = 11
pin_stepVertical = 15
pin_stepVerticalRight = 18
pin_stepPendulum = 29
pin_grabPendulum = 12

pin_directionHorizontal = 13
pin_directionVertical = 16
pin_directionVerticalRight = 22
pin_directionPendulum = 31

pin_sleep = 37

# Binary variables
sleepON = 1
sleepOFF = 0
directionLeft = 1
directionRight = 0
directionUp = 1
directionDown = 0
directionPendRaise = 1
directionPendLower = 0

# Initialize pinouts
gpio.setmode(gpio.BOARD)
gpio.setup(pin_sleep, gpio.OUT)
gpio.setup(pin_directionHorizontal, gpio.OUT)
gpio.setup(pin_directionVertical, gpio.OUT)
gpio.setup(pin_directionVerticalRight, gpio.OUT)
gpio.setup(pin_directionPendulum, gpio.OUT)
gpio.setup(pin_grabPendulum, gpio.OUT)
gpio.setup(pin_stepHorizontal, gpio.OUT)
gpio.setup(pin_stepVertical, gpio.OUT)
gpio.setup(pin_stepVerticalRight, gpio.OUT)
gpio.setup(pin_stepPendulum, gpio.OUT)

# Initialize sleep mode
gpio.output(pin_sleep, sleepON)

# Map test point positions in mm from center
# Common lie angles at address are 15, 16, and 17 degrees
# Row 1 is x coordinates (left to right)
Row 2 is y coordinates (top to bottom)
pts0_mm = np.matrix('-20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20; 10 10 10 10 10 10 10 10 10 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 -5 -5 -5 -5 -5 -5 -5 -5 -5 -10 -10 -10 -10 -10 -10 -10 -10 -10')
ang = math.radians(-90+15)
rotator = [[math.cos(ang), math.sin(ang)], [-(math.sin(ang)), math.cos(ang)]]
pts15_mm = np.matmul(rotator, pts0_mm)
ang = math.radians(1)
rotator = [[math.cos(ang), math.sin(ang)],
                     [-(math.sin(ang)), math.cos(ang)]]
pts16_mm = np.matmul(rotator, pts15_mm)
pts17_mm = np.matmul(rotator, pts16_mm)
ptsother_mm = pts0_mm

pts15_steps = pts15_mm
pts15_steps[0][:] *= mm2steps_horiz
pts15_steps[1][:] *= mm2steps_vert
pts15_steps[:][:] = np.round(pts15_steps[:][:])
pts15_steps = pts15_steps.astype(int)

pts16_steps = pts16_mm
pts16_steps[0][:] *= mm2steps_horiz
pts16_steps[1][:] *= mm2steps_vert
pts16_steps[:][:] = np.round(pts16_steps[:][:])
pts16_steps = pts16_steps.astype(int)

pts17_steps = pts17_mm
pts17_steps[0][:] *= mm2steps_horiz
pts17_steps[1][:] *= mm2steps_vert
pts17_steps[:][:] = np.round(pts17_steps[:][:])
pts17_steps = pts17_steps.astype(int)

ptsother_steps = ptsother_mm
ptsCurrent_steps = pts15_steps

# Initialize current position in steps from center
cp_steps = np.matrix('0; 0') # Current position
pendPos_steps = 0 # Pendulum postion


def donothing():    # Do nothing
    print("Do nothing")

# Reset position tracker to (0,0)
def calibrate():
    print("erase this out of claibrate() function")
    cp_steps[0,0] = 0
    cp_steps[1,0] = 0

# Swicth golfclub lie angles
def rotate(angle=15): # Positive angle is counterclockwise
    updateLabel_angle(angle)
    global ptsCurrent_steps
    if angle==15:
        ptsCurrent_steps = pts15_steps
    elif angle==16:
        ptsCurrent_steps = pts16_steps
    elif angle==17:
        ptsCurrent_steps = pts17_steps
    else:
        ang = math.radians(-90+angle)
        rotator = np.matrix([[math.cos(ang), math.sin(ang)],
                         [-(math.sin(ang)), math.cos(ang)]])
        ptsother_mm = np.matmul(rotator, pts0_mm)
        ptsother_steps = ptsother_mm
        ptsother_steps[0][:] *= mm2steps_horiz
        ptsother_steps[1][:] *= mm2steps_vert
        ptsother_steps[:][:] = np.round(pts17_steps[:][:])
        ptsother_steps = ptsother_steps.astype(int)
        ptsCurrent_steps = ptsother_steps   
# Move left
def stepLeft(dist=-99999):
    if dist == -99999:
        dist = -moveDist_horiz
    print(dist)
    cp_steps[0,0] += dist
    updateLabel_cp()
    if dist < 0:
        dist *= -1      
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionHorizontal, directionLeft)
    for x in range(dist):
            gpio.output(pin_stepHorizontal, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepHorizontal, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
# Move right
def stepRight(dist=99999):
    if dist == 99999:
        dist = moveDist_horiz
    print(dist)
    cp_steps[0,0] += dist
    updateLabel_cp()
    if dist < 0:
        dist *= -1
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionHorizontal, directionRight)
    for x in range(dist):
            gpio.output(pin_stepHorizontal, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepHorizontal, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
# Move up
def stepUp(dist=99999):
    if dist == 99999:
        dist = moveDist_vert
    print(dist)
    cp_steps[1,0] += dist
    updateLabel_cp()
    if dist < 0:
        dist *= -1
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionVertical, directionUp)
    gpio.output(pin_directionVerticalRight, directionUp)
    for x in range(dist):
            gpio.output(pin_stepVertical, 0)
            gpio.output(pin_stepVerticalRight, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepVertical, 1)
            gpio.output(pin_stepVerticalRight, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
# Move down
def stepDown(dist=-99999):
    if dist == -99999:
        dist = -moveDist_vert
    print(dist)
    cp_steps[1,0] += dist
    updateLabel_cp()
    if dist < 0:
        dist *= -1
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionVertical, directionDown)
    gpio.output(pin_directionVerticalRight, directionDown)
    for x in range(dist):
            gpio.output(pin_stepVertical, 0)
            gpio.output(pin_stepVerticalRight, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepVertical, 1)
            gpio.output(pin_stepVerticalRight, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
# Go to a specific test point 
def goto(point):
##    dist = np.subtract(ptsCurrent_steps[:,point], cp_steps)
    if dist[0,0] < 0:
        stepLeft(dist[0,0])
    elif dist[0,0] > 0:
        stepRight(dist[0,0])
    if dist[1,0] < 0:
        stepDown(dist[1,0])
    elif dist[1,0] > 0:
        stepUp(dist[1,0])  
# Raise the pendulum by 'height' number of steps
def raisePend(height=99999):
    if height == 99999:
        height = moveDist_pend
    print(height)
    global pendPos_steps
    pendPos_steps += height      
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionPendulum, directionPendRaise) 
    for x in range(height):
            gpio.output(pin_stepPendulum, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepPendulum, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
def lowerPend(height=99999):
    if height == 99999:
        height = moveDist_pend
    print(height)
    global pendPos_steps
    pendPos_steps -= height      
    gpio.output(pin_sleep, sleepOFF)
    gpio.output(pin_directionPendulum, directionPendLower) 
    for x in range(height):
            gpio.output(pin_stepPendulum, 0)
            time.sleep(sleeptime/2)
            gpio.output(pin_stepPendulum, 1)
            time.sleep(sleeptime/2)
    gpio.output(pin_sleep, sleepON)
# Drop the pendulum
pwm = gpio.PWM(pin_grabPendulum, freq_servo)
pwm.start(servoPos_dropped)
time.sleep(.3)
pwm.ChangeDutyCycle(0)
def dropPend():
    print("Drop pend")
    pwm.ChangeDutyCycle(servoPos_dropped)
    time.sleep(.5)
    pwm.ChangeDutyCycle(0)
# Grab the pendulum
def grabPend():
    print("Grab pend")
    pwm.ChangeDutyCycle(servoPos_grabbed)
    time.sleep(.5)
    pwm.ChangeDutyCycle(0)
# Test the current test point
def testPend():
    # Low height
    grabPend()
    time.sleep(0.3)
    raisePend(pend_lowHeight)
    time.sleep(0.3)
    dropPend()
    lowerPend(pendPos_steps)
    # Medium height
    grabPend()
    time.sleep(0.3)
    raisePend(pend_medHeight)
    time.sleep(0.3)
    dropPend()
    lowerPend(pendPos_steps)
    # High height
    grabPend()
    time.sleep(0.3)
    raisePend(pend_highHeight)
    time.sleep(0.3)
    dropPend()
    lowerPend(pendPos_steps)
# Test the 5 most at-risk test points
def RnD_test():
    progLabel = Label(top, textvariable=progress_label, bd=0)
    progLabel.place(relx=0.5, rely=0.2, anchor=N)
    # Center
    updateLabel_progress(1, 6)
    goto(center)
    testPend()
    # 20 Toe
    updateLabel_progress(2, 6)
    goto(toe20)
    testPend()
    # 10 Low
    updateLabel_progress(3, 6)
    goto(low10)
    testPend()
    # 20 Heel
    updateLabel_progress(4, 6)
    goto(heel20)
    testPend()
    # 10 High
    updateLabel_progress(5, 6)
    goto(high10)
    testPend()
    # 10 Toe / 10 High
    updateLabel_progress(6, 6)
    goto(toe10high10)
    testPend()
    progLabel.destroy()
# Test all test points (takes a while to complete)
def fullMap_test():
    for pt in range(0, 9, 1):
        goto(pt)
        testPend()
    for pt in range(17, 8, -1):
        goto(pt)
        testPend()
    for pt in range(18, 27, 1):
        goto(pt)
        testPend()
    for pt in range(35, 26, -1):
        goto(pt)
        testPend()
    for pt in range(36, 45, 1):
        goto(pt)
        testPend()
        
    
# Open the manual cotrol GUI
def manual():
    manual_menu = Toplevel(top)
    manual_menu.title(title_manual)
    manual_menu.geometry(menusize)
    manual_menu.resizable(FALSE,FALSE)
    def manual_back():
        manual_menu.destroy()
    def manual_calibrate():
        if messagebox.askyesno(title_calibrate, message_calibrate, parent=manual_menu) == True:
           #function(return): askquestion('yes' or 'no'), askokcancel(true or false), askyesno(true or false)
            calibrate()
            updateLabel_cp()
        else:
            pass
    def manual_goto():
        manual_goto_menu = Toplevel(manual_menu)
        manual_goto_menu.title(title_goto)
        manual_goto_menu.geometry(menusize)
        manual_goto_menu.resizable(FALSE,FALSE)
        def manual_goto_back():
            manual_goto_menu.destroy()
        Label(manual_goto_menu, textvariable=cp_mm_label, bd=0).place(relx=0.5, rely=0.137, anchor=N)
        manual_goto_backButton = tkinter.Button(manual_goto_menu, text="<-", bg=buttonColor,
                                                activebackground=bColor_active, command=manual_goto_back)
        manual_goto_backButton.pack()
        manual_goto_backButton.place(anchor=NW, relheight=buttonsize_relative/2,
                                     relwidth=buttonsize_relative/2)
        manual_goto_frame = Frame(manual_goto_menu, height=400, width=480)
        manual_goto_frame.place(x=gotogrid_offset_x, y=gotogrid_offset_y)
        for ctr in range(45):
            if ctr==heel20:
                point_button = Button(manual_goto_menu, text='"20 Heel"', height=buttonheight, width=buttonwidth,
                                     bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col) 
            elif ctr==center:
                point_button = Button(manual_goto_menu, text="Center", height=buttonheight, width=buttonwidth,
                                     bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)   
            elif ctr==toe20:
                point_button = Button(manual_goto_menu, text='"20 Toe"', height=buttonheight, width=buttonwidth,
                                  bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)
            elif ctr==high10:
                point_button = Button(manual_goto_menu, text='"10 High"', height=buttonheight, width=buttonwidth,
                                  bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)
            elif ctr==low10:
                point_button = Button(manual_goto_menu, text='"10 Low"', height=buttonheight, width=buttonwidth,
                                  bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)
            elif ctr==toe10high10:
                point_button = Button(manual_goto_menu, text='"10 Toe\n10 High"', height=buttonheight, width=buttonwidth,
                                  bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)
            else:
                point_button = Button(manual_goto_menu, text=str(ctr+1), height=buttonheight, width=buttonwidth,
                                      bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)     
    # Back button to closethe manual control menu
    manual_backButton = tkinter.Button(manual_menu, text="<-", bg=buttonColor, activebackground=bColor_active, command=manual_back)
    manual_backButton.pack()
    manual_backButton.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    # Left button in the manual control menu
    manual_leftButton = tkinter.Button(manual_menu, text = "Left", bg = buttonColor, activebackground=bColor_active, command=stepLeft)
    manual_leftButton.pack()
    manual_leftButton.place(relx=(1-buttonsize_relative)/2-buttonsize_relative, rely=buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Right button in the manual control menu
    manual_rightButton = tkinter.Button(manual_menu, text = "Right", bg=buttonColor, activebackground=bColor_active, command = stepRight)
    manual_rightButton.pack()
    manual_rightButton.place(relx=(1-buttonsize_relative)/2+buttonsize_relative, rely=buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Up button in the manual control menu
    manual_upButton = tkinter.Button(manual_menu, text = "Up", bg=buttonColor, activebackground=bColor_active, command = stepUp)
    manual_upButton.pack()
    manual_upButton.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Down button in the manual control menu
    manual_downButton = tkinter.Button(manual_menu, text="Down", bg=buttonColor, activebackground=bColor_active, command=stepDown)
    manual_downButton.pack()
    manual_downButton.place(relx=(1-buttonsize_relative)/2, rely=buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_lowerPendButton = tkinter.Button(manual_menu, text="Lower\nPendulum", bg=buttonColor, activebackground=bColor_active, command=lowerPend)
    manual_lowerPendButton.pack()
    manual_lowerPendButton.place(relx=0.5-0.5*buttonsize_relative, rely=buttonsize_relative, relheight=0.5*buttonsize_relative, relwidth=0.5*buttonsize_relative, anchor=SE)
    manual_raisePendButton = tkinter.Button(manual_menu, text="Raise\nPendulum", bg=buttonColor, activebackground=bColor_active, command=raisePend)
    manual_raisePendButton.pack()
    manual_raisePendButton.place(relx=0.5+0.5*buttonsize_relative, rely=buttonsize_relative, relheight=0.5*buttonsize_relative, relwidth=0.5*buttonsize_relative, anchor=SW)
    manual_dropPendButton = tkinter.Button(manual_menu, text="Drop\nPendulum", bg=buttonColor, activebackground=bColor_active, command=dropPend)
    manual_dropPendButton.pack()
    manual_dropPendButton.place(relx=0.5-0.5*buttonsize_relative, rely=0.5*buttonsize_relative, relheight=0.5*buttonsize_relative, relwidth=0.5*buttonsize_relative, anchor=SE)
    manual_grabPendButton = tkinter.Button(manual_menu, text="Grab\nPendulum", bg=buttonColor, activebackground=bColor_active, command=grabPend)
    manual_grabPendButton.pack()
    manual_grabPendButton.place(relx=0.5+0.5*buttonsize_relative, rely=0.5*buttonsize_relative, relheight=0.5*buttonsize_relative, relwidth=0.5*buttonsize_relative, anchor=SW)

    Label(manual_menu, textvariable=cp_mm_label, bd=0).place(relx=0.5, rely=buttonsize_relative*2, anchor=N)
    scale = Scale(manual_menu, label="Milimeters", bd=0, variable=scaleDist, orient=HORIZONTAL, length=300, resolution=steps2mm_horiz, to=5, command=getScaleMoveDist)
    scale.pack()
    scale.place(relx=0.5, rely=0.7, anchor=CENTER)

    # Button to open the Go-to-a-point menu
    manual_gotoButton = tkinter.Button(manual_menu, text="Go to position", bg=buttonColor, activebackground=bColor_active, command = manual_goto)
    manual_gotoButton.pack()
    manual_gotoButton.place(relx=(1-buttonsize_relative)/2, rely=1-buttonsize_relative/2, relheight=buttonsize_relative/2, relwidth=buttonsize_relative)
    # Positional calibration button the manual control menu
    manual_calibrateButton = tkinter.Button(manual_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=manual_calibrate)
    manual_calibrateButton.pack()
    manual_calibrateButton.place(relx=1-buttonsize_relative/2, rely=0, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
# Open the options GUI menu
def options():
    options_menu = Toplevel(top)
    options_menu.title(title_options)
    options_menu.geometry(menusize)
    def options_calibrate():
        if messagebox.askyesno(title_calibrate, message_calibrate, parent=options_menu) == True:
            calibrate()
            updateLabel_cp()
        else:
            pass
    def changeColor():
        # USE THIS FOR COLOR CALIBRATION
        dotColor = colorchooser.askcolor(parent=options_menu)
        print(dotColor)   
    def options_back():
        options_menu.destroy()
    # Back button in the options menu    
    options_backBtn = tkinter.Button(options_menu, text = "<-", bg=buttonColor, activebackground=bColor_active, command = options_back)
    options_backBtn.pack()
    options_backBtn.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    # Position calibration button in the options menu
    options_calibrateBtn = tkinter.Button(options_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=options_calibrate)
    options_calibrateBtn.pack()
    options_calibrateBtn.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Radio buttons to select lie angle at address
    options_pts15Btn = tkinter.Button(options_menu, text="15\nDegrees", bg=buttonColor, activebackground=bColor_active, command=lambda i=15: rotate(i) )
    options_pts15Btn.pack()
    options_pts15Btn.place(relx=(1-buttonsize_relative)/2-buttonsize_relative/4, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative/2)
    options_pts16Btn = tkinter.Button(options_menu, text="16\nDegrees", bg=buttonColor, activebackground=bColor_active, command=lambda i=16: rotate(i) )
    options_pts16Btn.pack()
    options_pts16Btn.place(relx=(1-buttonsize_relative)/2+buttonsize_relative*1/4, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative/2)
    options_pts17Btn = tkinter.Button(options_menu, text="17\nDegrees", bg=buttonColor, activebackground=bColor_active, command=lambda i=17: rotate(i) )
    options_pts17Btn.pack()
    options_pts17Btn.place(relx=(1-buttonsize_relative)/2+buttonsize_relative*3/4, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative/2)
    Label(options_menu, textvariable=angleLabel, bd=0).place(relx=0.5, rely=1-buttonsize_relative, anchor=S)

    

# Begin main program here
calibrate()

top = tkinter.Tk()
top.title(title_top)
top.geometry(menusize)
top.resizable(FALSE,FALSE)
##bgImage = PhotoImage(file="/home/pi/Desktop/golf.gif")
##bgTop = Label(image=bgImage)
##bgTop.grid(row=0, column=0)
##bgTop.lower()

def updateLabel_progress(progress=0, total=0):
    progress_label.set("Testing point %s of %s" %(progress, total))
    print("Testing point %s of %s" %(progress, total))
progress_label = StringVar()
def updateLabel_cp():
    print("erase this out of uptadeLabel_cp()")
    cp_mm_label.set("Current position: (%s, %s)mm" %(steps2mm_horiz*cp_steps[0,0], steps2mm_vert*cp_steps[1,0]))
cp_mm_label = StringVar()
updateLabel_cp()
def updateLabel_angle(angle):
    angleLabel.set("Lie angle at address: %s degrees" %angle)
angleLabel = StringVar()
updateLabel_angle(15)

def getScaleMoveDist(x):
    y = scaleDist.get()  
    global moveDist_vert
    moveDist_vert = round(y*mm2steps_vert)
    global moveDist_horiz
    moveDist_horiz = round(y*mm2steps_horiz)
    global moveDist_pend  
    moveDist_pend = round(y*mm2steps_pend)
    print("Move distance: %s" %y)
scaleDist = DoubleVar()
getScaleMoveDist(0)

# Button to open the manual control menu
manual_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Manual Control", bg=buttonColor, activebackground=bColor_active, command = manual)
manual_button.pack()
manual_button.place(relx=0.5-(buttonsize_relative)/2, rely=1, anchor=S, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to open the options menu
options_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Options", bg=buttonColor, activebackground=bColor_active, command = options)
options_button.pack()
options_button.place(relx=0.5+(buttonsize_relative)/2, rely=1, anchor=S, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the shortened R&D test
RnD_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text="R&D Standard\n(9 mins)", bg=buttonColor, activebackground=bColor_active, command=RnD_test)
RnD_button.pack()
RnD_button.place(relx=0, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on every single point
fullMap_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "USGA Full Map\n(68 mins)", bg=buttonColor, activebackground=bColor_active, command=fullMap_test)
fullMap_button.pack()
fullMap_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on the current point
single_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Single Point\n(2 min)", bg=buttonColor, activebackground=bColor_active, command = testPend)
single_button.pack()
single_button.place(relx=1-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

# tkinter's repeatdelay and repeatinterval values are in miliseconds

top.mainloop()
gpio.cleanup()
