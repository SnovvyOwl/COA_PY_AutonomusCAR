import socket

class Socketclient(object):
    def __init__(self,ip,port):
        self.host = ip# HOST address
        self.port = port #port number
        self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket Object is created 
        self.client_socket.connect((self.host,self.port))
        self.CMD = "None" # CMD
        self.status ="vel, angle" # Car's status
       
    def check(self):
        self.client_socket.send('I am a Client.'.encode('utf-8'))
        self.receive_CMD_and_send_status()
        print (self.CMD)
   
    def receive_CMD_and_send_status(self):
        data=self.client_socket.recv(1024) # 8Byte를 기다린다.
        self.CMD=data.decode()
        self.client_socket.send(self.status.encode('utf-8'))
    
    def connect_close(self):
        self.client_socket.close()


if __name__ == '__main__':
    client = Socketclient('192.168.35.125',8080)
    client.check()
    client.connect_close()
