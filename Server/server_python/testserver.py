import socket

class Socketserver(object):
    def __init__(self,ip,port):
        self.host = ip# HOST address
        self.port = port #port number
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket Object is created 
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # AVOID port error 
        self.server_socket.bind((self.host,self.port)) #client Binding
        self.server_socket.listen(1) # 1 Client is connectable
        self.status=""
       
    def check(self):
        print("Waiting Client")
        self.client_socket, self.addr = self.server_socket.accept()
        data = self.client_socket.recv(1024)  # 8Byte를 기다린다.
        check = data.decode()  # 속성 판단 receiver vs controller
        if check == "r":
            print("receiver is connected.",self.addr)
            self.status=check
    
    def receive_and_send_CMD(self):
        data=self.client_socket.recv(1024) # 8Byte를 기다린다.
        self.CMD=data.decode()
        #self.status=input("send data : ")
        #self.client_socket.send(self.status.encode('utf-8'))
    
    def connect_close(self):
        self.client_socket.close()
        self.server_socket.close()


if __name__ == '__main__':
    ss=Socketserver("192.168.42.64" ,8080)
    ss.check()
    print(ss.status)
    for i in range(10):
        msg="\r10,20,20,"+str(i)
        ss.client_socket.send(msg.encode("utf-8"))

    ss.connect_close()  