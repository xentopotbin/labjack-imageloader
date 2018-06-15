#!/usr/bin/python
#   Image loader with LabJack v1.1                                  #
#   Written 2017 by Virginia Heinen, Updated June 2018              #
#   Inspired by Mark Peterson & Tyler Blazey's C++ image loader     #
#   Uses LabJack digital reads to control a stimulus display        #
#                                                                   #
#####################################################################

import tkinter as tk
from PIL import Image, ImageTk
import u3   #from LabJack Python
import time
import os

class ImageLoader():
    def __init__(self):
        #create a tkinter root window
        self.root = tk.Tk()

        #remove title bar and other window theming
        self.root.overrideredirect(True)

        #make pointer invisible
        self.root.config(cursor='none')

        #Load up error images
        self.imageLJError =  ImageTk.PhotoImage(Image.open("labjack_error.png"))   #error image
        self.imageNotFound =  ImageTk.PhotoImage(Image.open("image_error.png"))  #error image

        #Load up numbered images and put them in a dictionary
        #Will read in all images saved as "XX.png" where XX is a number between 0 - 63
        self.imagedict= {}      #ake an empty dictionary

        self.files = os.listdir()     #lists all files in current directory

        for file in self.files:
            fileName = file.split('.')[0]
            if fileName.isdigit():
                fileName = int(fileName)
                self.imagedict[fileName] = ImageTk.PhotoImage(Image.open(file))

        #set desired window size
        w = 800
        h = 480

        #coordinates of upper left corner
        x = 0
        y = 0

        #list to hold lj reads
        self.lj = [0,0,0,0,0,0]

        #apply size and coordinates to root window
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        #display a blank image
        #Should be keyed to 0 in the dictionary
        self.panel1 = tk.Label(self.root,
        image=self.imagedict.get(0, self.imageNotFound))

        self.panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.currentImage = self.imagedict.get(0, self.imageNotFound)

        #Used to be a big "connect to labjack" section here
        #Let's see how well it works without it..

        #begin main loop
        self.root.after(50, self.read_labjack)
        self.root.mainloop()

    def initialize_labjack(self):
        try:
            self.d = u3.U3()                        #connect to labjack
            for x in range(0,7):                    #set FIO 0-7 to digital read
                self.d.getFeedback(u3.BitDirWrite(x,0))
        except TypeError:                           #LJ wasn't connected
            self.update_image(self.imageLJError)    #display LJ error message

    def update_image(self, newImage):   #only update if image has changed
        if self.currentImage != newImage:
            self.panel1.configure(image=newImage)
            self.currentImage = newImage

    def read_labjack(self):
        try:
            for x in range(0,6):
                self.lj[x] = self.d.getFIOState(x+1)    #read FIO 1 - 7
                #convert fron binary, invert because "on" lines read as 0
                self.ljNum= 63 - (self.lj[0] + self.lj[1]*2 + self.lj[2]*4 +
                self.lj[3]*8 + self.lj[4]*16 + self.lj[5]*32)
                #update with matching image from dictionary
                self.update_image(self.imagedict.get(self.ljNum, self.imageNotFound))

        except (u3.LabJackException, TypeError):  #No response from LJ?
            self.initialize_labjack()       #attempt to re-initialize
            time.sleep(0.3)                 #Don't need to poll so often
        finally:
            self.root.after(50, self.read_labjack)  #callback

def main():
    app = ImageLoader()

if __name__ == '__main__':
    main()
