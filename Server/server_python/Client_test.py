 import socket

class Client:
    def __init__(self):
        self.ip = "localhost"
        self.port = 5005

    def startClient(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address = (self.ip,self.port)
        sock.connect(server_address)

        try:
            message = 'This is the message.'
            print("sending " + message)
            sock.send(message.encode('utf-8'))

            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(1024)
                amount_received += len(data)
                print("received " + data.decode())

        finally:
            print("closing socket")
            sock.close()

if __name__ == '__main__':

    client = Client()
    client.startClient()
