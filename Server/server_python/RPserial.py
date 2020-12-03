import serial
import time
import RPi.GPIO as GPIO


class Serial_communication():
    def __init__(self,port='/dev/ttyUSB1'):
        #Serial communication information
        self.port = port
        self.baud = 115200
        self.timeout = 0
        
        #Serial communication data
        self.T_data = ""
        self.R_data = ""
        
        #Define serial communication
        self.ser = serial.Serial(self.port, self.baud, timeout = self.timeout)
    
    def Start_setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
        Channel_reset = 17          #To reset arduino, wiring GPIO15 to reset pin on arduino
        GPIO.setup(Channel_reset, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.output(Channel_reset, GPIO.LOW)        #Reset arduino
        time.sleep(1)
        GPIO.output(Channel_reset, GPIO.HIGH)
    
        self.Serial_check()
    
    def Serial_check(self, timeout = 5):
        i = 0
        while True:
            self.T_data = "TEST"
            self.Serial_write()
            time.sleep(1)
            print('Waiting serial connection.')
            self.Serial_read()
            if self.R_data == "TEST":
                self.R_data = ''
                break;
            elif i == timeout :
                print('Test fail');
                break;
            else:
                i += 1
    
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
        
if __name__ == '__main__':
    MySerial = Serial_communication()
    MySerial.Serial_check()
    while True:
        MySerial.T_data = input('input the code:')
        MySerial.Serial_write()
        
        while MySerial.R_data =='':
            MySerial.Serial_read()
        print(MySerial.R_data)
        time.sleep(1)
    