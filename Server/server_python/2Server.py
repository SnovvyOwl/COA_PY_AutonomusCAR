import socket

class SocketCommunication:
    def __init__(self):
        self.ip = "localhost"
        self.port = 5005
        self.clientNum = 1
        self.client = []

    def startServer(self):
        print("[start server]")
        print("Server ip ->", self.ip)
        print("Server port->", self.port)
        print(self.clientNum, "can connectable this server")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        sock.bind(server_address)
        sock.listen(self.clientNum)

        while True:
            # Wait for a connection
            connection, client_address = sock.accept()
            client = Client(connection, client_address)
            self.client.append(client)


class Client:
    def __init__(self, connection, clinet_address):
        self.connection = connection
        self.client_address = clinet_address
        self.receive()

    def receive(self):

        try:
            print("connection from",self.client_address)


            while True:
                data = self.connection.recv(1024)  # 8Byte를 기다린다.
                CMD = data.decode()
                print("controller: ",CMD)

                # print(CMD)
                # if input(">>") == "k":
                #     print("no more data")
                #     break
                # else:
                #     print("sending data back to client")
                #     self.send(CMD)

        finally:
            print("connection closed")
            self.connection.close()

    def send(self, data):
        self.connection.send(data.encode('utf-8'))


# class Controller(Client):
#     def __init__(self, connection, clinet_address):
#         super().__init__(connection, clinet_address)
#         self.receive()
#
#     def receive(self):
#
#         try:
#             print("connection from",self.client_address)
#
#             while True:
#                 data = self.connection.recv(1024)  # 8Byte를 기다린다.
#                 CMD = data.decode()
#                 print(CMD)
#
#                 # print(CMD)
#                 # if input(">>") == "k":
#                 #     print("no more data")
#                 #     break
#                 # else:
#                 #     print("sending data back to client")
#                 #     self.send(CMD)
#
#         finally:
#             print("connection closed")
#             self.connection.close()
#
#     def send(self, data):
#         self.connection.send(data.encode('utf-8'))


class main:

    server = SocketCommunication()
    server.startServer()