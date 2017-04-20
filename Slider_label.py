from tkinter import *

def sel(x):
   selection = "Value = " + str(var.get())
   label.config(text = selection)

root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var, command=sel )
scale.pack(anchor=CENTER)

label = Label(root)
label.pack()
label.config(text = selection)

root.mainloop()
