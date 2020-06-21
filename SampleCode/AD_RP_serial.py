import serial
import time

class Serial_command():
    def __init__(self):
        self.port = '/dev/ttyUSB0'
        self.baud = 115200
        self.timeout = 1
        self.T_data = ""
        self.T_data_history = ""
        self.R_data = ""
        self.ser = serial.Serial(self.port, self.baud, timeout = self.timeout)
    
    def Serial_check(self, timeout = 5):
        i = 0
        while True:
            self.T_data = "@TEST#"
            self.Serial_write()
            time.sleep(1)
            print('Waiting connection.')
            self.Serial_read()
            if self.R_data == "TEST":
                break;
            elif i == timeout :
                print('Test fail');
                break;
            else:
                i +=1
    
    def Serial_write(self):
        if self.T_data != self.T_data_history or self.T_data =='@TEST#':
            self.ser.write(self.T_data.encode("utf-8"))
            self.T_data_history = self.T_data
            self.T_data = ""
    
    def Serial_read(self):
        Temp = self.ser.readline()[:-2].decode('utf-8')
        if Temp:
            self.R_data = Temp
        else:
            self.R_data = ""
        
    def Value_to_T_data(self,BF,LR):
        BF_portion = ""
        LR_portion = ""
        
        if BF >= 0:
            BF_portion = "F" + str(BF)
        else:
            BF_portion = "B" + str(-BF)
        
        if LR >= 0:
            LR_portion = "R" + str(LR)
        else:
            LR_portion = "L" + str(-LR)
        
        self.T_data = '@' + BF_portion + LR_portion + '#'

class Position_status():
    def __init__(self):
        #BF, LR value is -500 to 500
        self.BF_desire = 0
        self.LR_desire = 500
        #self.BF_current = 10
        #self.LR_current = 10
        #self.BF_pulse = 1
        #self.LR_pulse = 2
    
    def Set_BF_position(self, value):
        self.BF_desire = value
    
    def Set_LR_position(self, value):
        self.LR_desire = value
    
    def Change_BF_position(self):
        if self.BF_desire > self.BF_current:
            self.BF_current = self.BF_current + self.BF_pulse
        if self.BF_desire < self.BF_current:
            self.BF_current = self.BF_current - self.BF_pulse
            
    def Change_LR_position(self):
        if self.LR_desire > self.LR_current:
            self.LR_current = self.LR_current + self.LR_pulse
        if self.LR_desire < self.LR_current:
            self.LR_current = self.LR_current - self.LR_pulse

if __name__ == '__main__':
    MySerial = Serial_command()
    MyPos = Position_status()

    #Start serial connection
    MySerial.Serial_check()

    #Serial command
    while True:
        
        if MyPos.LR_desire == 500:
            MyPos.LR_desire = -500
        elif MyPos.LR_desire == -500:
            MyPos.LR_desire = 500
    
        MySerial.Value_to_T_data(MyPos.BF_desire, MyPos.LR_desire)
        MySerial.Serial_write()
        MySerial.Serial_read()
        if MySerial.R_data != "":
            print(MySerial.R_data)
        time.sleep(2)
