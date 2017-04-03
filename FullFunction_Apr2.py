#import RPi.GPIO as gpio
import time
import sys
import math
#import numpy as np
from functools import partial

import tkinter
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import PhotoImage
from tkinter import *

# Variables for easy changes
menusize = '800x450-0+0'
buttonwidth = 9
buttonheight = 4
buttonsize_relative = 0.3

# Logo gold = "#d4bc20"
buttonColor = "#d48c20"
bColor_active = "#000000000"    #Pure black
dotColor = ((0.0, 255.99609375, 0.0), '#00ff00')

# Messages for easy changes
message_calibrate = "Make sure the golf clubface is centered before calibrating. This cannot be undone.\n\n Do you want to continue?"
title_top = 'Automated Clubface CT Tester'
title_calibrate = "Positional Calibration"
title_manual = 'Manual Control'
title_goto = 'Go To Point'
title_options = 'Options'

sleeptime = 2/1000 # In seconds

# Physical pins (as opposed to standard GPIO naming)
pin_stepHorizontal = 11
pin_stepVertical = 15
pin_stepVerticalRight = 18
pin_stepPendulum = 19

pin_directionHorizontal = 13
pin_directionVertical = 16
pin_directionVerticalRight = 22
pin_directionPendulum = 31

pin_sleep = 37
sleepON = 1
sleepOFF = 0

directionLeft = 1
directionRight = 0
directionUp = 1
directionDown = 0
directionPendRaise = 0
directionPendLower = 1

##gpio.setmode(gpio.BOARD)
##gpio.setup(pin_sleep, gpio.OUT)
##gpio.setup(pin_directionHorizontal, gpio.OUT)
##gpio.setup(pin_directionVertical, gpio.OUT)
##gpio.setup(pin_directionVerticalRight, gpio.OUT)
##gpio.setup(pin_directionPendulum, gpio.OUT)
##gpio.setup(pin_stepHorizontal, gpio.OUT)
##gpio.setup(pin_stepVertical, gpio.OUT)
##gpio.setup(pin_stepVerticalRight, gpio.OUT)
##gpio.setup(pin_stepPendulum, gpio.OUT)
##
##gpio.output(pin_sleep, sleepON)


##### UNTESTED AS OF APR 2ND, MIGHT BE BUGGY #################

# Create the maps for point positions in mm from center
# Common lie angles at address are 15, 16, and 17 degrees
# Row 1 is x coordinates (left to right)
# Row 2 is y coordinates (top to bottom)
##points_0 = np.matrix([[-20, -15, -5, 0, 5, 10, 15, 20, -20, -15, -5, 0, 5, 10, 15, 20, -20, -15, -5, 0, 5, 10, 15, 20, -20, -15, -5, 0, 5, 10, 15, 20, -20, -15, -5, 0, 5, 10, 15, 20],
##                      [10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, -5, -5, -5, -5, -5, -5, -5, -5, -10, -10, -10, -10, -10, -10, -10, -10, -10]])
##ang = math.radians(-15)
##rotator = np.matrix([[math.cos(ang), math.sin(ang)],
##                     [-(math.sin(ang)), math.cos(ang)]])
##points_15 = np.matmul(rotator, points_0)
##ang = math.radians(-1)
##rotator = np.matrix([[math.cos(ang), math.sin(ang)],
##                     [-(math.sin(ang)), math.cos(ang)]])
##points_16 = np.matmul(rotator, points_15)
##points_17 = np.matmul(rotator, points_16)
##points_other = points_0
##
##def rotate(angle):
##    if angle==15:
##        return points_15
##    elif angle==16:
##        return points_16
##    elif angle==17:
##        return points_17
##    else:
##        ang = math.radians(-angle)
##        rotator = np.matrix([[math.cos(ang), math.sin(ang)],
##                         [-(math.sin(ang)), math.cos(ang)]])
##        points_other = np.matmul(rotator, points_0)
##        return points_other
######## END UNTESTED SECTION ################################


def stepLeft():
##    gpio.output(pin_sleep, sleepOFF)
##    gpio.output(pin_directionHorizontal, directionLeft)
##    for x in range(0,99):
##        #while(buttonHeld == True)
##            gpio.output(pin_stepHorizontal, 0)
##            time.sleep(sleeptime/2)
##            gpio.output(pin_stepHorizontal, 1)
##            time.sleep(sleeptime/2)
##    gpio.output(pin_sleep, sleepON)
    print("Step left")

def stepRight():
##    gpio.output(pin_sleep, sleepOFF)
##    gpio.output(pin_directionHorizontal, directionRight)
##    for x in range(0,99):
##        #while(buttonHeld == True)
##            gpio.output(pin_stepHorizontal, 0)
##            time.sleep(sleeptime/2)
##            gpio.output(pin_stepHorizontal, 1)
##            time.sleep(sleeptime/2)
##    gpio.output(pin_sleep, sleepON)
    print("Step right")

def stepUp():
##    gpio.output(pin_sleep, sleepOFF)
##    gpio.output(pin_directionVertical, directionUp)
##    gpio.output(pin_directionVerticalRight, directionUp)
##    for x in range(0,99):
##        #while(buttonHeld == True)
##            gpio.output(pin_stepVertical, 0)
##            gpio.output(pin_stepVerticalRight, 0)
##            time.sleep(sleeptime/2)
##            gpio.output(pin_stepVertical, 1)
##            gpio.output(pin_stepVerticalRight, 1)
##            time.sleep(sleeptime/2)
##    gpio.output(pin_sleep, sleepON)
    print("Step up")

def stepDown():
##    gpio.output(pin_sleep, sleepOFF)
##    gpio.output(pin_directionVertical, directionDown)
##    gpio.output(pin_directionVerticalRight, directionDown)
##    for x in range(0,99):
##        #while(buttonHeld == True)
##            gpio.output(pin_stepVertical, 0)
##            gpio.output(pin_stepVerticalRight, 0)
##            time.sleep(sleeptime/2)
##            gpio.output(pin_stepVertical, 1)
##            gpio.output(pin_stepVerticalRight, 1)
##            time.sleep(sleeptime/2)
##    gpio.output(pin_sleep,     
    print("Step down")

def donothing():    # Do nothing
    print("Do nothing")

def calibrate():
    print("Insert positional calibration function here.")

def goto(point):
    print("Go to point %s" % (point) )

def manual():       # Open the manual controls mneu
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
        manual_goto_frame.place(x=72, y=80)

        for ctr in range(45):
            if ctr==22:
                point_button = Button(manual_goto_menu, text="23\n(Center)", height=buttonheight, width=buttonwidth,
                                     bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr+1))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)   
            else:
                point_button = Button(manual_goto_menu, text=str(ctr+1), height=buttonheight, width=buttonwidth,
                                      bg=buttonColor, activebackground=bColor_active, command=partial(goto, ctr+1))
                this_row, this_col = divmod(ctr,9)
                point_button.grid(in_=manual_goto_frame, row=this_row, column=this_col)   
         

    # Back button to closethe manual control menu
    manual_backButton = tkinter.Button(manual_menu, text="<-", bg=buttonColor, activebackground=bColor_active, command=manual_back)
    manual_backButton.pack()
    manual_backButton.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    # Left button in the manual control menu
    manual_leftButton = tkinter.Button(manual_menu, text = "Left", bg = buttonColor, activebackground=bColor_active, command=stepLeft)
    manual_leftButton.pack()
    manual_leftButton.place(relx=(1-buttonsize_relative)/2-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    #B4.bind('<Button-1>',stepLeft)
    #B4.bind('ButtonRelease-1',buttonOff)
    # Right button in the manual control menu
    manual_rightButton = tkinter.Button(manual_menu, text = "Right", bg=buttonColor, activebackground=bColor_active, command = stepRight)
    manual_rightButton.pack()
    manual_rightButton.place(relx=(1-buttonsize_relative)/2+buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Up button in the manual control menu
    manual_upButton = tkinter.Button(manual_menu, text = "Up", bg=buttonColor, activebackground=bColor_active, command = stepUp)
    manual_upButton.pack()
    manual_upButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Down button in the manual control menu
    manual_downButton = tkinter.Button(manual_menu, text="Down", bg=buttonColor, activebackground=bColor_active, command = stepDown)
    manual_downButton.pack()
    manual_downButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Button to open the Go-to-a-point menu
    manual_gotoButton = tkinter.Button(manual_menu, text="Go to position", bg=buttonColor, activebackground=bColor_active, command = manual_goto)
    manual_gotoButton.pack()
    manual_gotoButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2+1.25*buttonsize_relative, relheight=buttonsize_relative/2, relwidth=buttonsize_relative)
    # Positional calibration button the manual control menu
    manual_calibrateButton = tkinter.Button(manual_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=manual_calibrate)
    manual_calibrateButton.pack()
    manual_calibrateButton.place(relx=1-buttonsize_relative/2, rely=0, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)

def options():      # Open the options menu
    options_menu = Toplevel(top)
    options_menu.title(title_options)
    options_menu.geometry(menusize)

    def options_calibrate():
        if messagebox.askyesno(title_calibrate, message_calibrate, parent=options_menu) == True:
            calibrate()
        else:
            pass

    def changeColor():
        # USE THIS FOR COLOR CALIBRATION
        dotColor = colorchooser.askcolor(parent=options_menu)
        print(dotColor)
        
    def options_back():
        options_menu.destroy()

    # Back button in the options menu    
    options_backButton = tkinter.Button(options_menu, text = "<-", bg=buttonColor, activebackground=bColor_active, command = options_back)
    options_backButton.pack()
    options_backButton.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    # Tracking color chooser button in the options menu
    options_colorButton = tkinter.Button(options_menu, text = "Change Tracking Color", bg=buttonColor, activebackground=bColor_active, command = changeColor)
    options_colorButton.pack()
    options_colorButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    # Position calibration button in the options menu
    options_calibrateButton = tkinter.Button(options_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=options_calibrate)
    options_calibrateButton.pack()
    options_calibrateButton.place(relx=1-buttonsize_relative/2, rely=0, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)


# Begin main program here
top = tkinter.Tk()
top.title(title_top)
top.geometry(menusize)
top.resizable(FALSE,FALSE)
# Button to open the manual control menu
manual_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Manual Control", bg=buttonColor, activebackground=bColor_active, command = manual)
manual_button.pack()
manual_button.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to open the options menu
options_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Options", bg=buttonColor, activebackground=bColor_active, command = options)
options_button.pack()
options_button.place(relx=(1-buttonsize_relative)/2, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the shortened R&D test
RnD_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "R&D Standard", bg=buttonColor, activebackground=bColor_active, command = donothing)
RnD_button.pack()
RnD_button.place(relx=0, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on every single point
fullMap_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "USGA Full Map", bg=buttonColor, activebackground=bColor_active, command = donothing)
fullMap_button.pack()
fullMap_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
# Button to run the test on the current point
single_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Single Point", bg=buttonColor, activebackground=bColor_active, command = donothing)
single_button.pack()
single_button.place(relx=1-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

# tkinter's repeatdelay and repeatinterval values are in miliseconds

top.mainloop()
#gpio.cleanup()
