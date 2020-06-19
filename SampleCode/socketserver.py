import socket
import time

class Socketserver(object):
    def __init__(self):
        self.host = "127.0.0.1" # HOST address
        self.port = 4000 #port number
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket Object is created 
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # AVOID port error 
        self.server_socket.bind((self.host,self.port)) #client Binding
        self.server_socket.listen(1) # 1 Client is connectable
        self.CMD = "None" # CMD
        self.client_socket, self.addr = self.server_socket.accept()#클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
        self.status ="vel, angle" # Car's status
        print("Controler is Connected")
    
    def receive_CMD(self):
        data=self.client_socket.recv(8) # 8Byte를 기다린다.
        self.CMD=data.encode()
        self.client_socket.sendall(ength.to_bytes(8, byteorder="little")
        self.client_socket.sendall(self.status)
    
    def connect_close(self):
        self.client_socket.close()
        self.server_socket.close()


if __name__ == '__main__':
    ss=Socketserver()
    ss.receive_CMD()
    print(ss.CMD)
    ss.connect_close()
