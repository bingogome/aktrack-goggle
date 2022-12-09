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

from VOG import VOG
from connections import akConnections
from screendot import akScreenDot
import signal, time

class Application(akConnections):

    def __init__(self):
        super().__init__()
        width2, height2 = 1600, 1200
        self._VOG = VOG("C:\EyeTracker Debug 2018-22-08\EyeTrackerRemoteClient.dll")
        self._sd = akScreenDot(width2, height2)
        self._sd._VOG = self._VOG
        self.keyBindings()
        signal.signal(signal.SIGINT, self.clear)
        signal.signal(signal.SIGTERM, self.clear)

    def setup(self):
        super().setup()
        self._sd.setup()
        self._VOG.setup()
        
    def clear(self, *args):
        super().clear()
        self._sd._top.destroy()

    def receive(self):
        if self._flag_receiving:
            # print("receiving")
            try:
                self._data_buff = self._sock_receive.recv(128)
                self.handleReceivedData()
                self._sd._top.after(80, self.receive)
            except:
                self._sd._top.after(80, self.receive)

    def handleReceivedData(self):
        self.utilMsgParse()

    def keyBindings(self):
        self._sd._top.bind("q", lambda e: self.clear())
        self._sd._top.bind("c", lambda e: self.goggleCalibration())

    def utilSendTextCmdack(self, t):
        self._sock_send.sendto(
            t.encode('UTF-8'), (self._sock_ip, self._sock_port_send))
    
    def utilMsgParse(self):
        data = self._data_buff.decode("UTF-8")
        if data == "1":
            self.goggleVPBhfixedStart()
            self.utilSendTextCmdack("ack")
            print("VPB-hfixed")
        if data == "2":
            self.goggleVPBhfreeStart()
            self.utilSendTextCmdack("ack")
            print("VPB-hfree")
        if data == "3":
            self.goggleVPBhfixedEnd()
            self.utilSendTextCmdack("ack")
            print("VPB-hfixed end")
        if data == "4":
            self.goggleVPBhfreeEnd()
            self.utilSendTextCmdack("ack")
            print("VPB-hfree end")

    def goggleVPBhfixedStart(self):
        self._VOG.StartRecording()
        time.sleep(1) 
        self._VOG.RecordEvent('stat 1 start')

    def goggleVPBhfixedEnd(self):
        self._VOG.RecordEvent('stat 1 end')
        time.sleep(1) 
        self._VOG.StopRecording()

    def goggleVPBhfreeStart(self):
        self._VOG.StartRecording()
        time.sleep(1) 
        self._VOG.RecordEvent('stat 2 start')

    def goggleVPBhfreeEnd(self):
        self._VOG.RecordEvent('stat 2 end')
        time.sleep(1) 
        self._VOG.StopRecording()

    def goggleCalibration(self):
        if not self._sd._flag_calibrate:
            self._VOG.StartRecording()
            time.sleep(1) 
        else:
            self._VOG.StopRecording()
            time.sleep(1) 
        self._sd._flag_calibrate = self._sd._flag_calibrate != True
        print("Calibration: "+str(self._sd._flag_calibrate))
        
if __name__ == "__main__":
    app = Application()
    app.setup()