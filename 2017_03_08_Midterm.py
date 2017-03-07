import RPi.GPIO as gpio # Toolkit to control physical pins
import time
import sys

import tkinter # GUI toolkit
from tkinter import messagebox # Enables commands for a popup alert
from tkinter import *

sleeptime = 2/1000 # In seconds

#pin_ms0 = 29
#pin_ms1 = 31
#pin_ms2 = 33

pin_directionVertical = 16
pin_directionHorizontal = 18
pin_stepVertical = 11
pin_stepHorizontal = 13
pin_sleep = 22

directionLeft = 1
directionRight = 0
directionUp = 1
directionDown = 0

# Set up pin modes (OUT or IN)
gpio.setmode(gpio.BOARD) # BOARD mode means literal physical pin numbers
gpio.setup(pin_sleep, gpio.OUT)
gpio.setup(pin_directionHorizontal, gpio.OUT)
gpio.setup(pin_directionVertical, gpio.OUT)
gpio.setup(pin_stepHorizontal, gpio.OUT)
gpio.setup(pin_stepVertical, gpio.OUT)


def stepLeft():
        gpio.output(pin_directionHorizontal, directionLeft)
        gpio.output(pin_stepHorizontal, 0)
        time.sleep(sleeptime/2)
        gpio.output(pin_stepHorizontal, 1)
        time.sleep(sleeptime/2)

def stepRight():
        gpio.output(pin_directionHorizontal, directionRight)
        gpio.output(pin_stepHorizontal, 0)
        time.sleep(sleeptime/2)
        gpio.output(pin_stepHorizontal, 1)
        time.sleep(sleeptime/2)

def stepUp():
        gpio.output(pin_directionVertical, directionUp)
        gpio.output(pin_stepVertical, 0)
        time.sleep(sleeptime/2)
        gpio.output(pin_stepVertical, 1)
        time.sleep(sleeptime/2)

def stepDown():
        gpio.output(pin_directionVertical, directionDown)
        gpio.output(pin_stepVertical, 0)
        time.sleep(sleeptime/2)
        gpio.output(pin_stepVertical, 1)
        time.sleep(sleeptime/2)

def runStandard():
   print("This is where the standard test sequence would run...")
def runFullMap():
   print("This is where the high resolution test sequence would run...")
def runSinglePoint():
   print("This is where the single-point test sequence would run...")




def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do Nothing")
   button.pack()

# Buttons for manual cotrol
#def Button_stepLeft():
#    filewin = Toplevel(root)
#    button = Button(filewin, text="Left", command = stepLeft)
#    button.pack()
#def Button_stepRight():
#    filewin = Toplevel(root)
#    button = Button(filewin, text="Right", command = stepRight)
#    button.pack()
#def Button_stepUp():
#    filewin = Toplevel(root)
#    button = Button(filewin, text="Up", command = stepUp)
#    button.pack()
#def Button_stepDown():
#    filewin = Toplevel(root)
#    button = Button(filewin, text="Down", command = stepDown)
#    button.pack()

# Buttons for automatic testing    
#def Button_Standard():
#   filewin = Toplevel(root)
#   button = Button(filewin, text="GO", command = runStandard)
#   button.pack()
#def Button_FullMap():
#   filewin = Toplevel(root)
#   button = Button(filewin, text="GO", command = runFullMap)
#   button.pack()
#def Button_SinglePoint():
#   filewin = Toplevel(root)
#   button = Button(filewin, text="GO", command = runSinglePoint)
#   button.pack()




messagebox.showinfo("Notice", "Please center the face of the golf club before pressing a test button!") #Should this line go below the next one?
top = tkinter.Tk()
B1 = tkinter.Button(top, text = "R&D Standard", bg = "#000fff000", activebackground = "#000000", command = runStandard)
B1.pack()
B2 = tkinter.Button(top, text = "USGA Full Map", bg = "#000fff000", activebackground = "#000000", command = runFullMap)
B2.pack()
B3 = tkinter.Button(top, text = "Single Point", bg = "#000fff000", activebackground = "#000000", command = runSinglePoint)
B3.pack()

B4 = tkinter.Button(top, text = "Left", bg = "#000fff000", activebackground = "#000000", command = stepLeft)
B4.pack()
B5 = tkinter.Button(top, text = "Right", bg = "#000fff000", activebackground = "#000000", command = stepRight)
B5.pack()
B6 = tkinter.Button(top, text = "Up", bg = "#000fff000", activebackground = "#000000", command = stepUp)
B6.pack()
B7 = tkinter.Button(top, text = "Down", bg = "#000fff000", activebackground = "#000000", command = stepDown)
B7.pack()


# Pick up editing here to add buttons for the main menue / front page of
# the illustrative GUI powerpoint created on Feb 18, 2017

# Everything below here is from the menus example I found online
root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# GUI scripts usualy end with this
root.mainloop()










#infinite_loop = True
#while (infinite_loop == True):
#        set_stepper_on()
        

#GPIO.ceanup()


