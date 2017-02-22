import tkinter
from tkinter import messagebox
from tkinter import *


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
def StandardButton():
   filewin = Toplevel(root)
   button = Button(filewin, text="GO", command = runStandard)
   button.pack()
def FullMapButton():
   filewin = Toplevel(root)
   button = Button(filewin, text="GO", command = runFullMap)
   button.pack()
def SinglePointButton():
   filewin = Toplevel(root)
   button = Button(filewin, text="GO", command = runSinglePoint)
   button.pack()

messagebox.showinfo("Notice", "Please center the face of the golf club before pressing a test button!") #Should this line go below the next one?
top = tkinter.Tk()
B1 = tkinter.Button(top, text = "R&D Standard", bg = "#000fff000", activebackground = "#000000", command = runStandard)
B1.pack()
B2 = tkinter.Button(top, text = "USGA Full Map", bg = "#000fff000", activebackground = "#000000", command = runFullMap)
B2.pack()
B3 = tkinter.Button(top, text = "Single Point", bg = "#000fff000", activebackground = "#000000", command = runSinglePoint)
B3.pack()

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
