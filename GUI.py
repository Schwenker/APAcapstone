import time
import sys

import tkinter
from tkinter import messagebox
from tkinter import *


def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do Nothing")
   button.pack()


#def options_menu():
#    windowname = 

#messagebox.showinfo("Notice", "Please center the face of the golf club before pressing a test button!") #Should this line go below the next one?


top = tkinter.Tk()



RnD_button = tkinter.Button(top, text = "R&D Standard", bg = "#000fff000", activebackground = "#000000", command = donothing)
RnD_button.pack()

fullMap_button = tkinter.Button(top, text = "USGA Full Map", bg = "#000fff000", activebackground = "#000000", command = donothing)
fullMap_button.pack()

single_button = tkinter.Button(top, text = "Single Point", bg = "#000fff000", activebackground = "#000000", command = donothing)
single_button.pack()

back_button = tkinter.Button(top, text = "<- BACK", bg = "#000fff000", activebackground = "#000000", command = donothing)
back_button.pack()

options_button = tkinter.Button(top, text = "OPTIONS", bg = "#000fff000", activebackground = "#000000", command = donothing)

# tkinter's repeatdelay and repeatinterval values are in miliseconds
B4 = tkinter.Button(top, text = "Left", bg = "#000fff000", activebackground = "#000000", command = stepLeft)
B4.pack()
#B4.bind('<Button-1>',stepLeft)
#B4.bind('ButtonRelease-1',buttonOff)
B5 = tkinter.Button(top, text = "Right", bg = "#000fff000", activebackground = "#000000", command = stepRight)
B5.pack()
B6 = tkinter.Button(top, text = "Up", bg = "#000fff000", activebackground = "#000000", command = stepUp)
B6.pack()
B7 = tkinter.Button(top, text = "Down", bg = "#000fff000", activebackground = "#000000", command = stepDown)
B7.pack()







# Everything below here is from the menus example I found online
##root = Tk()
##menubar = Menu(root)
##filemenu = Menu(menubar, tearoff=0)
##filemenu.add_command(label="New", command=donothing)
##filemenu.add_command(label="Open", command=donothing)
##filemenu.add_command(label="Save", command=donothing)
##filemenu.add_command(label="Save as...", command=donothing)
##filemenu.add_command(label="Close", command=donothing)
##
##filemenu.add_separator()
##
##filemenu.add_command(label="Exit", command=root.quit)
##menubar.add_cascade(label="File", menu=filemenu)
##editmenu = Menu(menubar, tearoff=0)
##editmenu.add_command(label="Undo", command=donothing)
##
##editmenu.add_separator()
##
##editmenu.add_command(label="Cut", command=donothing)
##editmenu.add_command(label="Copy", command=donothing)
##editmenu.add_command(label="Paste", command=donothing)
##editmenu.add_command(label="Delete", command=donothing)
##editmenu.add_command(label="Select All", command=donothing)
##
##menubar.add_cascade(label="Edit", menu=editmenu)
##helpmenu = Menu(menubar, tearoff=0)
##helpmenu.add_command(label="Help Index", command=donothing)
##helpmenu.add_command(label="About...", command=donothing)
##menubar.add_cascade(label="Help", menu=helpmenu)
##
##root.config(menu=menubar)




top.mainloop()


