from HW_controller.socketclient import Socketclient
from HW_controller.AD_RP_serial import *
import threading


class Car(object):
    def __init__(self):
        self.client=Socketclient("192.168.137.91",8080)
        self.serial=Serial_communication()
        self.pos= Position_status()
    
    def check(self):
        self.serial.Serial_check()
        self.client.check()
        self.th = threading.Thread(target=self.client.receive_CMD_and_send_status, args = (self.client))
        self.th.start()

    def run(self):
        while (self.client.CMD != 'q'):
            Start_point = time.time()
            self.pos.Set_BF_position(0)
            self.pos.Set_LR_position(0)
            self.serial.Value_to_T_data(self.pos.BF_desire, self.pos.LR_desire)
            self.serial.Serial_write()
            self.serial.Serial_read()
            if self.serial.R_data != "":
                print(self.serial.R_data)
            End_point = time.time()
            time.sleep(self.serial.Loop_time-(End_point-Start_point))
            

if __name__ == '__main__':
    car= Car()
    car.check()
    car.run()