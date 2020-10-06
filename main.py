from socketserver import *
from RPserial import *
from Car import *

class TimeController():
    def __init__(self,looptime = 0.02):
        self.startpoint = 0
        self.endpoint = 0
        self.looptime = looptime
    
    def Set_startpoint(self):
        self.startpoint = time.time()
    
    def Set_endpoint(self):
        self.endpoint = time.time()
        
    def Set_sleeptime(self):
        Temp = self.looptime - (self.endpoint-self.startpoint)
        if Temp > 0:
            return Temp
        else:
            return 0

if __name__ == '__main__':
    ss=Socketserver("172.20.10.2" ,8080)
    MySerial = Serial_communication()
    MyTime = TimeController()
    
    MySerial.Start_setup()
    
    while True:
        MyTime.Set_startpoint
        
        ss.check()
        print('pi received by android : ' + ss.CMD)
        ss.connect_close()
        
        MySerial.T_data = ss.CMD
        MySerial.Serial_write()
        print('pi sent to arduino :' + ss.CMD)
        while MySerial != "I'm client":
            MySerial.Serial_read()
        print('pi received by arduino :' + MySerial.R_data)
        
        
        MyTime.Set_endpoint
        time.sleep(MyTime.Set_sleeptime())
        
        