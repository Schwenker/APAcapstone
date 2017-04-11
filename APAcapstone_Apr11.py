## Updated: Apr 11, 2017
## To do:
## Add button + entry-box for arbitrary lie-angles 
## Add entry box to choose move distance per press of manual direction buttons
## Fill in placeholder functions to control the pendulum

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
steps2mm_horiz = 1/mm2steps_horiz
steps2mm_vert = 1/mm2steps_vert

# GUI sizes and colors
menusize = '800x450-0+0'
buttonwidth = 6
buttonheight = 4
buttonsize_relative = 0.3
gotogrid_offset_x = 55
gotogrid_offset_y = 80
# Logo gold = "#d4bc20"
buttonColor = "#ffd700" #also gold
bColor_active = "#000000000"    #Pure black
dotColor = ((0.0, 255.99609375, 0.0), '#00ff00')

# Messages and titles
message_calibrate = "Make sure the golf clubface is centered before calibrating. This cannot be undone.\n\n Do you want to continue?"
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
pin_stepPendulum = 19

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
directionPendRaise = 0
directionPendLower = 1

# Initialize pinouts
gpio.setmode(gpio.BOARD)
gpio.setup(pin_sleep, gpio.OUT)
gpio.setup(pin_directionHorizontal, gpio.OUT)
gpio.setup(pin_directionVertical, gpio.OUT)
gpio.setup(pin_directionVerticalRight, gpio.OUT)
gpio.setup(pin_directionPendulum, gpio.OUT)
gpio.setup(pin_stepHorizontal, gpio.OUT)
gpio.setup(pin_stepVertical, gpio.OUT)
gpio.setup(pin_stepVerticalRight, gpio.OUT)
gpio.setup(pin_stepPendulum, gpio.OUT)

# Initialize sleep mode
gpio.output(pin_sleep, sleepON)

# Map test point positions in mm from center
# Common lie angles at address are 15, 16, and 17 degrees
# Row 1 is x coordinates (left to right)
# Row 2 is y coordinates (top to bottom)
pts0_mm = np.matrix('-20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20 -20 -15 -10 -5 0 5 10 15 20; 10 10 10 10 10 10 10 10 10 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 -5 -5 -5 -5 -5 -5 -5 -5 -5 -10 -10 -10 -10 -10 -10 -10 -10 -10')
ang = math.radians(-15)
rotator = [[math.cos(ang), math.sin(ang)], [-(math.sin(ang)), math.cos(ang)]]
pts15_mm = np.matmul(rotator, pts0_mm)
ang = math.radians(-1)
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
cp_steps = np.matrix('0; 0')


def donothing():    # Do nothing
    print("Do nothing")

# Reset position tracker to (0,0)
def calibrate():
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
        ang = math.radians(-angle)
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
def stepLeft(dist=-100):
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
def stepRight(dist=100):
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
def stepUp(dist=100):
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
def stepDown(dist=-100):
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
    print("Go to point: %s" %point)
    dist = np.subtract(ptsCurrent_steps[:,point], cp_steps)
    if dist[0,0] < 0:
        stepLeft(dist[0,0])
    elif dist[0,0] > 0:
        stepRight(dist[0,0])
    if dist[1,0] < 0:
        stepDown(dist[1,0])
    elif dist[1,0] > 0:
        stepUp(dist[1,0])  
# Raise the pendulum by 'height' number of steps
def raisePend(height):
    print("Raise pendulum to height: %s" %height)
    time.sleep(1)
# Drop the pendulum
def dropPend():
    print("Drop pendulum")
    time.sleep(.5)
# Test the current test point
def testPend():
    raisePend("low")
    dropPend()
    raisePend("med")
    dropPend()
    raisePend("high")
    dropPend()
# Test the 5 most at-risk test points
def RnD_test():
    goto(18)
    testPend()
    goto(26)
    testPend()
    goto(40)
    testPend()
    goto(4)
    testPend()
    goto(2)
    testPend()
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
        manual_goto_backButton = tkinter.Button(manual_goto_menu, text="<-", bg=buttonColor,
                                                activebackground=bColor_active, command=manual_goto_back)
        manual_goto_backButton.pack()
        manual_goto_backButton.place(anchor=NW, relheight=buttonsize_relative/2,
                                     relwidth=buttonsize_relative/2)
        manual_goto_frame = Frame(manual_goto_menu, height=400, width=480)
        manual_goto_frame.place(x=gotogrid_offset_x, y=gotogrid_offset_y)
        for ctr in range(45):
            if ctr==22:
                point_button = Button(manual_goto_menu, text="23\n(Center)", height=buttonheight, width=buttonwidth,
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
    #B4.bind('<Button-1>',stepLeft)
    #B4.bind('ButtonRelease-1',buttonOff)
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
    
    Label(manual_menu, textvariable=cp_mm_label, bd=0).place(relx=0.5, rely=buttonsize_relative*2, anchor=N)

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
    # Tracking color chooser button in the options menu
##    options_colorBtn = tkinter.Button(options_menu, text = "Change Tracking Color", bg=buttonColor, activebackground=bColor_active, command = changeColor)
##    options_colorBtn.pack()
##    options_colorBtn.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
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

def updateLabel_cp():
    cp_mm_label.set("Current position: (%s, %s)mm" %(steps2mm_horiz*cp_steps[0,0], steps2mm_vert*cp_steps[1,0]))
cp_mm_label = StringVar()
updateLabel_cp()
def updateLabel_angle(angle):
    angleLabel.set("Lie angle at address: %s degrees" %angle)
angleLabel = StringVar()
updateLabel_angle(15)

# Button to open the manual control menu
manual_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Manual Control", bg=buttonColor, activebackground=bColor_active, command = manual)
manual_button.pack()
manual_button.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to open the options menu
options_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Options", bg=buttonColor, activebackground=bColor_active, command = options)
options_button.pack()
options_button.place(relx=(1-buttonsize_relative)/2, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the shortened R&D test
RnD_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "R&D Standard", bg=buttonColor, activebackground=bColor_active, command=RnD_test)
RnD_button.pack()
RnD_button.place(relx=0, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on every single point
fullMap_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "USGA Full Map", bg=buttonColor, activebackground=bColor_active, command=fullMap_test)
fullMap_button.pack()
fullMap_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on the current point
single_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Single Point", bg=buttonColor, activebackground=bColor_active, command = donothing)
single_button.pack()
single_button.place(relx=1-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

# tkinter's repeatdelay and repeatinterval values are in miliseconds

top.mainloop()
gpio.cleanup()
