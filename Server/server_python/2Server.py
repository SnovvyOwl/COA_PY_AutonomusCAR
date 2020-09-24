from threading import Thread
import socket


class SocketCommunication:
    def __init__(self):
        self.ip = "localhost"
        self.port = 5005
        self.clientNum = 5

        self.receiver = []
        self.controller = []

        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startServer(self):
        print("[start server]")
        print("Server ip ->", self.ip)
        print("Server port->", self.port)
        print(self.clientNum, "can connectable this server")

        server_address = (self.ip, self.port)
        self.mSocket.bind(server_address)
        self.mSocket.listen(self.clientNum)

        while True:
            # Wait for a connection
            connection, client_address = self.mSocket.accept()
            data = connection.recv(1024)  # 8Byte를 기다린다.
            check = data.decode()

            print("connection from", client_address)

            if (check == "c"):
                print("controller", len(self.controller), "is connected.")

                mClient = Thread(target= Client, args= (connection,client_address))
                # mClient = Client(connection, client_address)
                self.controller.append(mClient)
                mClient.start()
                mClient.join()

            elif (check == "r"):
                print("receiver", len(self.receiver), "is connected.")
                mClient = Client(connection, client_address)
                self.receiver.append(mClient)

            else:
                print("Illegal connection has detected.")
                connection.close()

    def stopServer(self):
        print("[stop server]")
        print("- Thank you -")
        self.mSocket.close()


class Client:
    def __init__(self, connection, client_address):
        self.connection = connection
        self.client_address = client_address

    def receive(self):

        try:
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

        except ConnectionResetError:
            print("disconnection from client")


        finally:
            print("connection closed")
            self.connection.close()

    def send(self, data):
        self.connection.send(data.encode('utf-8'))


class Receiver(Client):
    def __init__(self,connection,client_address):
        super().__init__(connection, client_address)
        self.receive()


class Controller(Client):
    def __init__(self,connection,client_address):
        super(Controller, self).__init__(connection,client_address)



class main:

    server = SocketCommunication()
    server.startServer()