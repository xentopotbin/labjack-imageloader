# labjack-imageloader

This program displays images based on readings from a [LabJack U3-LV](https://labjack.com/products/u3), though it should be easy to modify for other LabJack models. It is designed for a 800x480 screen such as [this one](https://www.adafruit.com/product/2406). Digital inputs 1-7 are used as binary bits to determine which image is displayed.

I used this program to "translate" output from a [MED Associates](http://www.med-associates.com/) interface panel through the LabJack, essentially allowing the screen display to be controlled by a MED program.

### Prerequisites

* [LabJack Python](https://labjack.com/support/software/examples/ud/labjackpython)
* [Tkinter](https://wiki.python.org/moin/TkInter)
* [ImageTK](https://pillow.readthedocs.io/en/4.2.x/reference/ImageTk.html)

### Getting Started

Your images should be in the same folder as the python script.  Images should exactly 800x480.
The images must be named appropriately in order to be read.  There should be two "error" images, named "labjack_error.png" and "image_error.png".

All other images should be named "XX.png", where XX is a number between 0-63.  The "blank" or "default" image, to be displayed when there is no input to the LabJack, should be 00.png.  Other images will be displayed when their number is read from the LabJack.

On the LabJack, FI01 - FI07 correspond to binary bits 1 - 32.  When used with a MED-PC tower, connect FI00 to ground.  Connect FI01 - FI07 to the center control pins of the desired MED tower outputs.  When an outputs is turned "on", that pin will be connected to ground and read low.  

## Acknowledgments

* HeatfanJohn's answer about [Tkinter](https://raspberrypi.stackexchange.com/questions/18261/how-do-i-display-an-image-file-png-in-a-simple-window).
* Mark Peterson & Tyler Blazey wrote the old C++ image loader that inspired this project.
