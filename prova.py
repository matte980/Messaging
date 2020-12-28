import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('84.222.52.81', 8022))
clientsocket.send('hello')