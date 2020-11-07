# 실제 사용시 최상위폴더로 옮겨질 필요가 있음.
import socket
import sys
from multiprocessing import Process, Queue, freeze_support
from HW_controller.AD_RP_serial import *
import time
class Client:
    def __init__(self):
        #Socket
        self.ip = "bluetank.iptime.org"# need to change server IP
        self.port = 13000
        self.sock=""
        
        #Serial
        self.arduino = Serial_communication('/dev/ttyACM0') 
        self.position = Position_status()

    def receive(self, toclient):
        data = self.sock.recv(8)
        toclient.put(data.decode())    
        
    def send(self,toserver):
        msg = toserver.get()
        self.sock.sendall(msg.encode('utf-8'))

    def startClient(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address = (self.ip,self.port)
        self.sock.connect(server_address)
        print("start")
        try:

            if (self.arduino.Start_setup()==1):
                sys.exit()
            #self.server_msg(message)
            message = 'r'
            print("sending " + message)
            self.sock.send(message.encode('utf-8'))
            print("run Client")
            self.runClient()
        except ConnectionResetError:
            print("Disconnect from Server")

        
    def runClient(self):
        try:
            send_msg = Queue()
            recive_msg = Queue()

            while True:
                sending= Process(target=self.send, args=(send_msg,))
                Start_point=time.time()
                sending.start()
                reciveing=Process(target=self.receive,args=(recive_msg,))
                reciveing.start()
                reciveing.join()
                command=recive_msg.get()
                reciveing.close()
                print(command)
                if command=="Test":
                    self.position.LR_desire=255
                    self.position.BF_desire=0
                    #print(self.position.LR_desire)
                    
                elif command=="call":
                    self.position.LR_desire=-255
                    self.position.BF_desire=0
                    #print(self.position.LR_desire)
                elif command=="quit":
                    sys.exit()
                    
                    
                # Arduino Parts
                Start_point = time.time()
                self.arduino.Value_to_T_data(self.position.BF_desire, self.position.LR_desire)
                self.arduino.Serial_write()
                time.sleep(1)
                self.arduino.Serial_read()
                if self.arduino.R_data != "":
                    #print(self.arduino.R_data)
                    send_msg.put(self.arduino.R_data)
                    sending.join()
                    sending.close()
                     
                #End_point = time.time()
                #time.sleep(self.arduino.Loop_time-(End_point-Start_point))
                
        
        except KeyboardInterrupt:
            print("Emergency stop!!!!")
            self.sock.close()
            reciveing.terminate()
            sending.terminate()
            reciveing.close()
            sending.close()
            
        finally:
            print("OFF")
            self.sock.close()
 

if __name__ == '__main__':
    freeze_support()
    client = Client()
    client.startClient()
