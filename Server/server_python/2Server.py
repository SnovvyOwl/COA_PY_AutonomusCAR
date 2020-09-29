import socket
from threading import Thread


class SocketCommunication:
    def __init__(self, ip=None, port=None):
        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip is None:
            self.ip = "localhost"
        if port is None:
            self.port = 5005
            return
        self.ip = ip
        self.port = port

    def startServer(self):
        print("[start server]")
        print("Server ip ->", self.ip)
        print("Server port->", self.port)
        # print("\n",, "can connectable this server")

        server_address = (self.ip, self.port)
        self.mSocket.bind(server_address)
        self.mSocket.listen(2)

    def stopServer(self):
        print("[stop server]")
        print("- Thank you -")
        self.mSocket.close()

    def showInfo(self):
        print(self.ip, self.port)


class Client:
    def __init__(self, connection, clinet_address):
        self.connection = connection
        self.client_address = clinet_address
        # self.receive()

        # self.thread = Thread(self.receive())
        # self.thread.start()

    def receive(self):
        try:
            while True:
                data = self.connection.recv(1024)  # 8Byte를 기다린다.
                CMD = data.decode()
                print("controller: ", CMD)

        except ConnectionResetError:
            # self.thread.close()
            print("disconnect from client")

        finally:
            self.connection.close()
            # self.thread.close()
            print("connection closed")

    def send(self, data):
        self.connection.send(data.encode('utf-8'))


if __name__ == '__main__':
    receiverNum = 0
    controllerNum = 0

    server = SocketCommunication()
    server.startServer()

    try:
        while KeyboardInterrupt:
            # Wait for a connection
            print("wait")
            connection, client_address = server.mSocket.accept()
            data = connection.recv(1024)  # 8Byte를 기다린다.
            check = data.decode()  # 속성 판단 receiver vs controller

            print("connection from", client_address)

            if check == "c":
                print("controller is connected.")
                thread = Thread(target=Client, args=(connection, client_address))
                thread.start()

            elif check == "r":
                print("receiver is connected.")
                thread = Thread(target=Client, args=(connection, client_address))
                thread.start()

            else:
                print("Illegal connection has detected.")
                connection.close()

    except KeyboardInterrupt:
        server.stopServer()
        print("이게 맞았으면 좋겠댱...")
        pass