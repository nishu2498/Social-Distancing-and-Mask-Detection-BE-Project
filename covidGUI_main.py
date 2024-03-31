# -*- coding: utf-8 -*-
"""
Created on

@author: 
"""

import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as ms
import cv2
import sqlite3
import os
import numpy as np
import time


global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="brown")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Covid Mask And Social Distancing System")

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('covid.png')
image2 = image2.resize((1530, 900), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) 
#
label_l1 = tk.Label(root, text="Covid Mask And Social Distancing System",font=("Times New Roman", 35, 'bold'),
                    background="#152238", fg="white", width=50, height=2)
label_l1.place(x=60, y=0)



def reg():
    from subprocess import call
    print("Social Distancing module called!!!")
    call(["python","socialdistance.py"])

def log():
    from subprocess import call
    print("Detect Mask Video module called!!!")
    call(["python","detect_mask_video.py"])
    
def window():
  root.destroy()


button1 = tk.Button(root, text="Covid Mask Detection", command=log, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
button1.place(x=100, y=160)

button2 = tk.Button(root, text="Social Distancing", command=reg, width=14, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
button2.place(x=100, y=240)

button3 = tk.Button(root, text="Exit",command=window,width=14, height=1,font=('times', 20, ' bold '), bg="#152238", fg="white")
button3.place(x=100, y=330)

root.mainloop()