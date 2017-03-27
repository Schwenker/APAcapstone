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
dotColor = ((0.0, 255.99609375, 0.0), '#00ff00')

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
    manual_leftButton = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Left", bg = colorGreen, activebackground = "#000000", command = donothing)
    manual_leftButton.pack()
    manual_leftButton.place(relx=(1-buttonsize_relative)/2-buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    #B4.bind('<Button-1>',stepLeft)
    #B4.bind('ButtonRelease-1',buttonOff)
    manual_rightButton = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Right", bg = "#000fff000", activebackground = "#000000", command = donothing)
    manual_rightButton.pack()
    manual_rightButton.place(relx=(1-buttonsize_relative)/2+buttonsize_relative, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_upButton = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text = "Up", bg = "#000fff000", activebackground = "#000000", command = donothing)
    manual_upButton.pack()
    manual_upButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2-buttonsize_relative, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_downButton = tkinter.Button(manual_menu, height=buttonheight, width=buttonwidth, text="Down", bg="#000fff000", activebackground = "#000000", command = donothing)
    manual_downButton.pack()
    manual_downButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2, relheight=buttonsize_relative, relwidth=buttonsize_relative)
    manual_tposButton = tkinter.Button(manual_menu, text="Type in a position", bg="#000fff000", activebackground = "#000000", command = donothing)
    manual_tposButton.pack()
    manual_tposButton.place(relx=(1-buttonsize_relative)/2, rely=(1-buttonsize_relative)/2+1.25*buttonsize_relative, relheight=buttonsize_relative/2, relwidth=buttonsize_relative)
    manual_menu.mainloop()
def options():
    options_menu = Toplevel(top)
    def changeColor():
        # USE THIS FOR COLOR CALIBRATION
        top.iconify()
        options_menu.lower()
        dotColor = colorchooser.askcolor()
        print(dotColor)
        top.deiconify()
        options_menu.lift()
    def options_back():
        options_menu.destroy()
    options_menu.title('Options')
    options_menu.geometry(menusize)
    options_backButton = tkinter.Button(options_menu, height=buttonheight, width=buttonwidth, text = "<-", bg = "#000fff000", activebackground = "#000000", command = options_back)
    options_backButton.pack()
    options_backButton.place(anchor=NW)
    options_colorButton = tkinter.Button(options_menu, text = "Change Tracking Color", bg = "#000fff000", activebackground = "#000000", command = changeColor)
    options_colorButton.pack()
    options_colorButton.place
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
