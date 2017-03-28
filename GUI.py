import time
import sys

import tkinter
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import PhotoImage
from tkinter import *

# Variables for easy changes
menusize = '800x450-0+0'
buttonwidth = 20
buttonheight = 4
buttonsize_relative = 0.3

# Logo gold = '#d4bc20'
buttonColor = "#d48c20"
bColor_active = "#000000000"    #Pure black
dotColor = ((0.0, 255.99609375, 0.0), '#00ff00')

# Messages for easy changes
message_calibrate = "Make sure the golf clubface is centered before calibrating. This cannot be undone.\n\n Do you want to continue?"
title_calibrate = "Positional Calibration"

#main_background = PhotoImage(file="golf.jpg")


def donothing():    # Do nothing
    print("Do nothing")

def manual():       # Open the manual controls mneu
    manual_menu = Toplevel(top)
    def manual_back():
        manual_menu.destroy()
    def manual_calibrate():
        if messagebox.askyesno(title_calibrate, message_calibrate, parent=manual_menu) == True:
            print("Insert positional calibration function here.")
        else:
            pass
    #function(return): askquestion('yes' or 'no'), askokcancel(true or false), askyesno(true or false)
    manual_menu.title('Manual Control')
    manual_menu.geometry(menusize)
    manual_menu.resizable(FALSE,FALSE)
    manual_backButton = tkinter.Button(manual_menu, text="<-", bg=buttonColor, activebackground=bColor_active, command=manual_back)
    manual_backButton.pack()
    manual_backButton.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    manual_leftButton = tkinter.Button(manual_menu, text = "Left", bg = buttonColor, activebackground=bColor_active, command = donothing)
    manual_leftButton.pack()
    manual_leftButton.place(relx=(1-buttonsize_relative)/2-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    #B4.bind('<Button-1>',stepLeft)
    #B4.bind('ButtonRelease-1',buttonOff)
    manual_rightButton = tkinter.Button(manual_menu, text = "Right", bg=buttonColor, activebackground=bColor_active, command = donothing)
    manual_rightButton.pack()
    manual_rightButton.place(relx=(1-buttonsize_relative)/2+buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_upButton = tkinter.Button(manual_menu, text = "Up", bg=buttonColor, activebackground=bColor_active, command = donothing)
    manual_upButton.pack()
    manual_upButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_downButton = tkinter.Button(manual_menu, text="Down", bg=buttonColor, activebackground=bColor_active, command = donothing)
    manual_downButton.pack()
    manual_downButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_tposButton = tkinter.Button(manual_menu, text="Type in a position", bg=buttonColor, activebackground=bColor_active, command = donothing)
    manual_tposButton.pack()
    manual_tposButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2+1.25*buttonsize_relative, relheight=buttonsize_relative/2, relwidth=buttonsize_relative)
    manual_calibrateButton = tkinter.Button(manual_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=manual_calibrate)
    manual_calibrateButton.pack()
    manual_calibrateButton.place(relx=1-buttonsize_relative/2, rely=0, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
def options():      # Open the options menu
    options_menu = Toplevel(top)
    def options_calibrate():
        if messagebox.askyesno(title_calibrate, message_calibrate, parent=options_menu) == True:
            print("Insert positional calibration function here.")
        else:
            pass
    def changeColor():
        # USE THIS FOR COLOR CALIBRATION
        #top.iconify()
        #options_menu.lower()
        dotColor = colorchooser.askcolor(parent=options_menu)
        print(dotColor)
        #top.deiconify()
        #options_menu.lift()
    def options_back():
        options_menu.destroy()
    options_menu.title('Options')
    options_menu.geometry(menusize)
    options_backButton = tkinter.Button(options_menu, text = "<-", bg=buttonColor, activebackground=bColor_active, command = options_back)
    options_backButton.pack()
    options_backButton.place(anchor=NW, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)
    options_colorButton = tkinter.Button(options_menu, text = "Change Tracking Color", bg=buttonColor, activebackground=bColor_active, command = changeColor)
    options_colorButton.pack()
    options_colorButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    options_calibrateButton = tkinter.Button(options_menu, text = "Calibrate\nClub Position", bg=buttonColor, activebackground=bColor_active, command=options_calibrate)
    options_calibrateButton.pack()
    options_calibrateButton.place(relx=1-buttonsize_relative/2, rely=0, relheight=buttonsize_relative/2, relwidth=buttonsize_relative/2)


top = tkinter.Tk()


top.title('Automated Clubface CT Tester')
top.geometry(menusize)
top.resizable(FALSE,FALSE)


manual_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Manual Control", bg=buttonColor, activebackground=bColor_active, command = manual)
manual_button.pack()
manual_button.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)

options_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Options", bg=buttonColor, activebackground=bColor_active, command = options)
options_button.pack()
options_button.place(relx=(1-buttonsize_relative)/2, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)


RnD_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "R&D Standard", bg=buttonColor, activebackground=bColor_active, command = donothing)
RnD_button.pack()
RnD_button.place(relx=0, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

fullMap_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "USGA Full Map", bg=buttonColor, activebackground=bColor_active, command = donothing)
fullMap_button.pack()
fullMap_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

single_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Single Point", bg=buttonColor, activebackground=bColor_active, command = donothing)
single_button.pack()
single_button.place(relx=1-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

# tkinter's repeatdelay and repeatinterval values are in miliseconds



top.mainloop()
