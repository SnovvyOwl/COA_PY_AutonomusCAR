import serial
import time
import RPi.GPIO as GPIO

Loop_time = 0.05

class Serial_command():
    def __init__(self):
        #Serial communication information
        self.port = '/dev/ttyUSB0'
        self.baud = 115200
        self.timeout = 0.005
        
        #Serial communication data
        self.T_data = ""
        self.T_data_history = ""
        self.R_data = ""
        
        #Define serial communication
        self.ser = serial.Serial(self.port, self.baud, timeout = self.timeout)
    
    def Serial_check(self, timeout = 5):
        i = 0
        while True:
            self.T_data = "TEST"
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
        if self.T_data != self.T_data_history or self.T_data =='TEST':
            self.ser.write('@'.encode('utf-8') + self.T_data.encode("utf-8") + '#'.encode('utf-8'))
            self.T_data_history = self.T_data
            self.T_data = ""
    
    def Serial_read(self):
        Temp = self.ser.read().decode('utf-8')
        if Temp == '@':
            self.R_data = ''
            while True:
                Temp = self.ser.read().decode('utf-8')
                if Temp == '#':
                    break
                elif Temp != '@' and Temp != '#' and Temp != '':
                    self.R_data = self.R_data + Temp
                else:
                    pass
        else:
            self.R_data = ''
        
    def Value_to_T_data(self,BF,LR):
        BF_position = ""
        LR_position = ""
        
        if BF >= 0:
            BF_position = "F" + str(BF)
        else:
            BF_position = "B" + str(-BF)
        
        if LR >= 0:
            LR_position = "R" + str(LR)
        else:
            LR_position = "L" + str(-LR)
        
        self.T_data = BF_position + LR_position

class Position_status():
    def __init__(self):
        #BF, LR value range is -255 to 255
        self.BF_desire = 100
        self.LR_desire = 0
        #self.BF_current = 10
        #self.LR_current = 10
        #self.BF_pulse = 1
        #self.LR_pulse = 2
    
    def Set_BF_position(self, value):
        self.BF_desire = value
    
    def Set_LR_position(self, value):
        self.LR_desire = value
    
    #deactivated function for a while
    #def Change_position(self):
        #if self.BF_desire > self.BF_current:
            #self.BF_current = self.BF_current + self.BF_pulse
        #if self.BF_desire < self.BF_current:
            #self.BF_current = self.BF_current - self.BF_pulse
        #if self.LR_desire > self.LR_current:
            #self.LR_current = self.LR_current + self.LR_pulse
        #if self.LR_desire < self.LR_current:
            #self.LR_current = self.LR_current - self.LR_pulse

def Start_setup():
    #CAUTION, MySerial must be defined at main code(MySerial = Serial_command())
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    Channel_reset = 17          #To reset arduino, wiring GPIO15 to reset pin on arduino
    GPIO.setup(Channel_reset, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.output(Channel_reset, GPIO.LOW)        #Reset arduino
    time.sleep(1)
    GPIO.output(Channel_reset, GPIO.HIGH)
    
    Channel_flag = 27
    GPIO.setup(Channel_flag, GPIO.OUT, initial = GPIO.HIGH)
    
    MySerial.Serial_check()

if __name__ == '__main__':
    MySerial = Serial_command()
    MyPos = Position_status()

    #Start serial connection and set GPIO pin etc
    Start_setup()
    i = 0
    speed = [200, 0, -200, 0]
    #Serial command
    while True:
        Start_point = time.time()
        
        if i == 3:
            MyPos.BF_desire = speed[i]
            i = 0
        else:
            MyPos.BF_desire = speed[i]
            i += 1
        
        MySerial.Value_to_T_data(MyPos.BF_desire, MyPos.LR_desire)
        MySerial.Serial_write()
        MySerial.Serial_read()
        if MySerial.R_data != "":
            print(MySerial.R_data)
        
        End_point = time.time()
        time.sleep(Loop_time-(End_point-Start_point))
        #print(End_point-Start_point)
