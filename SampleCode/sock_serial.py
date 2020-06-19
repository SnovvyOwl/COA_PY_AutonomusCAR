from socketserver import Socketserver
from AD_RP_serial import *
import threading

class Car(object):
    def __init__(self):
        self.server=Socketserver()
        self.serial=Serial_command()
        self.pos= Position_status()
    
    def check(self):
        self.serial.Serial_check()
        self.server.check()
        self.th = threading.Thread(target=server.receive_CMD, args = (server.client_socket,server.addr))
        self.th.start()

    def run(self):
        while (server.CMD != 'q'):
            self.pos.Change_BF_position()
            self.pos.Change_LR_position()
            self.serial.Value_to_T_data(self.pos.BF_current, self.pos.LR_current)
            if self.serial.T_data_history != self.serial.T_data:
                print(self.serial.T_data)
            self.serial.Serial_write()
            self.serial.Serial_read()
            if self.serial.R_data != "":
                print(self.serial.R_data)
            time.sleep(0.001)
            

if __name__ == '__main__':
    car= Car()
    car.check()
    car.run()