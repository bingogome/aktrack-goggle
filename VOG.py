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

import clr, time

class VOG:

    def __init__(self, eyeTrackerDllPath):
        self.eyeTracker = None
        self.eyeTrackerDll = None
        self.eyeTrackerDllPath = eyeTrackerDllPath
    def setup(self):
        self.eyeTrackerDll = clr.AddReference(self.eyeTrackerDllPath)
        from VORLab.VOG.Remote import EyeTrackerClient
        self.eyeTracker = EyeTrackerClient("10.17.101.204", 9000)
    
    def IsRecording(self):
        status = self.eyeTracker.Status
        result = status.Recording
        return result
    
    def SetSessionName(self, sessionName):
        if self.eyeTracker:
            self.eyeTracker.ChangeSetting('SessionName',sessionName)
        
    def StartRecording(self):
        if self.eyeTracker:
            self.eyeTracker.StartRecording()
    
    def StopRecording(self):
        if self.eyeTracker:
            self.eyeTracker.StopRecording()
    
    def RecordEvent(self, message):
        frameNumber = []
        if self.eyeTracker:
            t = time.time()
            frameNumber = self.eyeTracker.RecordEvent(str(t) + ' ' + message)
            frameNumber = float(frameNumber)
        return frameNumber

if __name__ == "__main__":
    app = VOG("C:\EyeTracker Debug 2018-22-08\EyeTrackerRemoteClient.dll")
    app.setup()
