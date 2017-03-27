import time
import sys

import tkinter
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import *

menusize = '800x450-0+0'
buttonwidth = 20
buttonheight = 4
buttonsize_relative = 0.3

colorGreen = "#000fff000"

def donothing():
    print("Do nothing")


def manual():
    manual_menu = Toplevel(top)
    def manual_back():
        manual_menu.destroy()
    manual_menu.title('Manual Control')
    manual_menu.geometry(menusize)
    manual_menu.resizable(FALSE,FALSE)
    manual_backButton = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text="<-", bg="#000fff000", activebackground="#000000", command=manual_back)
    manual_backButton.pack()
    manual_backButton.place(anchor=NW)
    left_button = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Left", bg = colorGreen, activebackground = "#000000", command = donothing)
    left_button.pack()
    left_button.place(relx=(1-buttonsize_relative)/2-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    #B4.bind('<Button-1>',stepLeft)
    #B4.bind('ButtonRelease-1',buttonOff)
    right_button = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Right", bg = "#000fff000", activebackground = "#000000", command = donothing)
    right_button.pack()
    right_button.place(relx=(1-buttonsize_relative)/2+buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    up_button = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Up", bg = "#000fff000", activebackground = "#000000", command = donothing)
    up_button.pack()
    up_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    down_button = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Down", bg = "#000fff000", activebackground = "#000000", command = donothing)
    down_button.pack()
    down_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_menu.mainloop()
def options():
    options_menu = Toplevel(top)
    def changeColor():
        # USE THIS FOR COLOR CALIBRATION
        colorchooser.askcolor(initialcolor='#ff0000')
        options_menu.lift()
    def options_back():
        options_menu.destroy()
    options_menu.title('Options')
    options_menu.geometry(menusize)
    options_backButton = tkinter.Button(options_menu, height=buttonheight, width=buttonwidth, text = "<-", bg = "#000fff000", activebackground = "#000000", command = options_back)
    options_backButton.pack()
    options_backButton.place(anchor=NW)
    options_colorButton = tkinter.Button(options_menu, height=buttonheight, width=buttonwidth, text = "Change Tracking Color", bg = "#000fff000", activebackground = "#000000", command = changeColor)
    options_colorButton.pack()
    options_menu.mainloop()


#def options_menu():
#    windowname = 

#messagebox.showinfo("Notice", "Please center the face of the golf club before pressing a test button!") #Should this line go below the next one?


top = tkinter.Tk()
top.title('Automated Clubface CT Tester')
top.geometry(menusize)
top.resizable(FALSE,FALSE)


manual_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Manual Control", bg = "#000fff000", activebackground = "#000000", command = manual)
manual_button.pack()
manual_button.place(relx=(1-buttonsize_relative)/2, rely=0, relheight=buttonsize_relative, relwidth=buttonsize_relative)

options_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Options", bg = "#000fff000", activebackground = "#000000", command = options)
options_button.pack()
options_button.place(relx=(1-buttonsize_relative)/2, rely=1-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)


RnD_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "R&D Standard", bg = "#000fff000", activebackground = "#000000", command = donothing)
RnD_button.pack()
RnD_button.place(relx=0, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

fullMap_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "USGA Full Map", bg = "#000fff000", activebackground = "#000000", command = donothing)
fullMap_button.pack()
fullMap_button.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

single_button = tkinter.Button(top, height=buttonheight, width=buttonwidth, text = "Single Point", bg = "#000fff000", activebackground = "#000000", command = donothing)
single_button.pack()
single_button.place(relx=1-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)

# tkinter's repeatdelay and repeatinterval values are in miliseconds



top.mainloop()
