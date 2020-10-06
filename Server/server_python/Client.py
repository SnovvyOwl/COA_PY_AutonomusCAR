# 실제 사용시 최상위폴더로 옮겨질 필요가 있음.
import socket
from multiprocessing import Process, Queue, freeze_support
from HW_controller.AD_RP_serial import *
import time
class Client:
    def __init__(self):
        #Socket
        self.ip = "localhost" # need to change server IP
        self.port = 5005
        self.sock=""
        
        #Serial
        self.arduino = Serial_communication() 
        self.position = Position_status()

    def receive(self, toclient):
        message = "r"
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = self.sock.recv(1024)
            amount_received += len(data)
            #print("received " + data.decode())
            amount_received = 0
        toclient.put(data.decode())    
        
    def send(self,toserver):
        msg = toserver.get()
        self.sock.send(msg.encode('utf-8'))

    def startClient(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address = (self.ip,self.port)
        self.sock.connect(server_address)

        try:
            message = 'r'
            print("sending " + message)
            self.sock.send(message.encode('utf-8'))
            self.arduino.Start_setup()
            #self.server_msg(message)
    
        except ConnectionResetError:
            print("Disconnect from Server")

        finally:
            print("run Client")
            self.runClient()

        
    def runClient(self):
        try:
            send_msg = Queue()
            recive_msg = Queue()
            sending= Process(target=self.send, args=(send_msg))
            reciveing=Process(target=self.receive,arg=(recive_msg))
            sending.start()
            reciveing.start()
            while True:
                reciveing.join()
                command=recive_msg.get()

                # Arduino Parts
                Start_point = time.time()
                self.arduino.Value_to_T_data(self.position.BF_desire, self.position.LR_desire)
                self.arduinoSerial_write()
                self.arduinoSerial_read()
                if self.arduino.R_data != "":
                    print(self.arduino.R_data)
                    send_msg.put(self.arduino.R_data)
                    send_msg.join()
                End_point = time.time()
                time.sleep(self.arduino.Loop_time-(End_point-Start_point))
                reciveing.run()
                send_msg.run()      
        
        except KeyboardInterrupt:
            print("Emergency stop!!!!")
            self.sock.close()
            reciveing.close()
            send_msg.close()    
        finally:
            print("OFF")
            self.sock.close()
            reciveing.close()
            send_msg.close()    

if __name__ == '__main__':
    freeze_support()
    client = Client()
    client.startClient()