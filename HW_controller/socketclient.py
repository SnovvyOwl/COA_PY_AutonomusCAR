import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.35.125',8080))

client.send('I am CLIENT\n'.encode())

from_server = client.recv(4096)
client.close()
print (from_server)
#print (num)