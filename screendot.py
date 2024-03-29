"""
MIT License
Copyright (c) 2022 Yihao Liu, Johns Hopkins University
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter
import winsound

class akScreenDot:
    
    def __init__(self, width2, height2):

        self._top = tkinter.Tk()
        self._top.title("Goggle")
        self._dot = None
        self.monitorInfo(width2, height2)
        self.canvasSettings()
        self.keyBindings()

        self._flag_calibrate = False
        self._flag_fullscreen = False

    def monitorInfo(self, width2, height2):
        self._width1= self._top.winfo_screenwidth()
        self._height1= self._top.winfo_screenheight()
        self._width2 = width2
        self._height2 = height2
        self._top.geometry(f"{self._width2}x{self._height2}")
        # self._top.geometry(f"+0-{self._height2}") # use this to change the window location

    def canvasSettings(self):
        self._canvas = tkinter.Canvas(self._top, bg="black", \
            width=self._width2, height=self._height2, \
            highlightthickness=0, bd=0)
        self._outlinewidth = 16
        self._rad = 10 + self._outlinewidth/2
        
    def keyBindings(self):
        self._top.bind("a",  lambda e: self.fullScreen())
        self._top.bind("d",  lambda e: self.visualStimulusInit())
        self._top.bind("s",  lambda e: self.visualStimulusMotion(1))
        self._top.bind("<KeyPress-Right>",  lambda e: self.visualStimulusMotion(2))
        self._top.bind("<KeyPress-Left>",  lambda e: self.visualStimulusMotion(3))
        self._top.bind("<KeyPress-Up>",  lambda e: self.visualStimulusMotion(4))
        self._top.bind("<KeyPress-Down>",  lambda e: self.visualStimulusMotion(5))
        self._top.bind("<Escape>",  lambda e: self.visualStimulusStop())
        self._top.bind("q", lambda e: self.cleanUp())
        
    def setup(self):
        self._canvas.pack()
        self._top.mainloop()

    def clear(self, *args):
        self._top.destroy()
    
    def cleanUp(self):
        self.clear()

    def fullScreen(self, e=None):
        if not self._flag_fullscreen:
            self._top.attributes("-topmost", 1)
            self._top.attributes("-fullscreen", True)
        else:
            self._top.attributes("-topmost", 0)
            self._top.attributes("-fullscreen", False)
        self._flag_fullscreen = self._flag_fullscreen != True

    def visualStimulusSet(self, coor):
        if self._dot:
            self._canvas.delete(self._dot)
            self._canvas.delete('all')
            self._dot = None
            self._canvas.config(bg="black", \
                width=self._width2, height=self._height2, \
                highlightthickness=0, bd=0)
            self._canvas.pack()
        self._dot = self._canvas.create_oval(\
            coor[0], coor[1], coor[2], coor[3], \
            fill = "red",
            outline = "black", 
            width=self._outlinewidth)

    def visualStimulusInit(self, e=None):
        # get a large width to deal with the cutoff of the dot
        # For future developer: try the width = 0 and move it at a hi speed
        coor = [\
            self._width2/2-self._rad, self._height2/2-self._rad, \
            self._width2/2+self._rad, self._height2/2+self._rad \
            ]
        self.visualStimulusSet(coor)

    def visualStimulus(self, e=None):
        self.visualStimulusInit()
        self._canvas.itemconfig(self._dot, fill = "red")

    def visualStimulusMotion(self, dir=5, e=None):
        self.visualStimulus()
        if dir == 1:
            self._xpos, self._ypos = 0.5 * self._width2, 0.5 * self._height2
        if dir == 2:
            self._xpos, self._ypos = 0.78 * self._width2, 0.5 * self._height2
            cal_msg = "right start"
        if dir == 3:
            self._xpos, self._ypos = 0.22 * self._width2, 0.5 * self._height2
            cal_msg = "left start"
        if dir == 4:
            self._xpos, self._ypos = 0.5 * self._width2, 0.22 * self._height2
            cal_msg = "up start"
        if dir == 5:
            self._xpos, self._ypos = 0.5 * self._width2, 0.78 * self._height2
            cal_msg = "down start"
        coor = [\
            self._xpos-self._rad, self._ypos-self._rad, \
            self._xpos+self._rad, self._ypos+self._rad \
            ]
        winsound.Beep(400, 500) # f, t
        self.visualStimulusSet(coor)
        if self._flag_calibrate:
            self._VOG.RecordEvent(cal_msg)
    
    def visualStimulusStop(self):
        if self._flag_calibrate:
            self._VOG.RecordEvent("end")
        self._canvas.delete(self._dot)
        self._canvas.delete('all')
        self._dot = None
        self._canvas.config(bg="black", \
            width=self._width2, height=self._height2, \
            highlightthickness=0, bd=0)
        self._canvas.pack()
        winsound.Beep(400, 500) # f, t

if __name__ == "__main__":
    # Use monitorenum.py to determine the second monitor size and locations
    width2, height2 = 1200, 800
    sd = akScreenDot(width2, height2)
    sd.setup()
