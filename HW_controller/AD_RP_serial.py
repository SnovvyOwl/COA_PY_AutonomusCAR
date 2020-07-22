import serial
import time
import RPi.GPIO as GPIO


class Serial_command():
    def __init__(self):
        #Serial communication information
        self.port = '/dev/ttyUSB0'
        self.baud = 115200
        self.timeout = 0
        
        #Serial communication data
        self.T_data = ""
        self.R_data = ""
        
        #Define serial communication
        self.ser = serial.Serial(self.port, self.baud, timeout = self.timeout)
        
        self.Loop_time = 0.02
    
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
        self.ser.write('@'.encode('utf-8') + self.T_data.encode("utf-8") + '#'.encode('utf-8'))
    
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
    
    def Set_BF_position(self, value):
        self.BF_desire = value
    
    def Set_LR_position(self, value):
        self.LR_desire = value

def Start_setup():
    #CAUTION, MySerial must be defined at main code(MySerial = Serial_command())
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    Channel_reset = 17          #To reset arduino, wiring GPIO15 to reset pin on arduino
    GPIO.setup(Channel_reset, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.output(Channel_reset, GPIO.LOW)        #Reset arduino
    time.sleep(1)
    GPIO.output(Channel_reset, GPIO.HIGH)
    
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
        
        MyPos.BF_desire = speed[0]
        
        MySerial.Value_to_T_data(MyPos.BF_desire, MyPos.LR_desire)
        MySerial.Serial_write()
        MySerial.Serial_read()
        if MySerial.R_data != "":
            print(MySerial.R_data)
        End_point = time.time()
        time.sleep(MySerial.Loop_time-(End_point-Start_point))
        
#Current Serial read method must be improved. Because, When I use
#Serial read twice time within one loop, It cause improper situation.
