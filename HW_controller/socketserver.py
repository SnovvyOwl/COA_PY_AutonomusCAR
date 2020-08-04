import socket

class Socketserver(object):
    def __init__(self,ip,port):
        self.host = ip# HOST address
        self.port = port #port number
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket Object is created 
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # AVOID port error 
        self.server_socket.bind((self.host,self.port)) #client Binding
        self.server_socket.listen(1) # 1 Client is connectable
        self.CMD = "None" # CMD
        self.status ="vel, angle" # Car's status
       
    def check(self):
        print("Waiting Client")
        self.client_socket, self.addr = self.server_socket.accept() #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
        print("Controler is Connected",self.addr)
        self.receive_and_send_CMD()
        self.client_socket.send('I am a server.'.encode('utf-8'))
        print('메시지를 보냈습니다.')
    
    def receive_and_send_CMD(self):
        data=self.client_socket.recv(1024) # 8Byte를 기다린다.
        self.CMD=data.decode()
        #self.status=input("send data : ")
        #self.client_socket.send(self.status.encode('utf-8'))
    
    def connect_close(self):
        self.client_socket.close()
        self.server_socket.close()


if __name__ == '__main__':
    ss=Socketserver("192.168.35.125" ,8080)
    ss.check()
    print(ss.CMD)
    """
    while(True):
        ss.receive_and_send_CMD()
        print(ss.CMD)
        if(ss.CMD=="q"):
            break
    """
    ss.connect_close()