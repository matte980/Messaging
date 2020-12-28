#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
import threading

# class StoppableThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""

#     def __init__(self,  *args, **kwargs):
#         super(StoppableThread, self).__init__(*args, **kwargs)
#         self._stop_event = threading.Event()

#     def stop(self):
#         self._stop_event.set()

#     def stopped(self):
#         return self._stop_event.is_set()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Holaaa, scrivi il tuo nome almeno so chi sei", "utf8"))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = 'Matteo'
    # name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! To exit type {quit}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# def joinThread(tt):
#     global kill_flag
#     if kill_flag: SERVER.close()
#     else: tt.join()
#     return

# def askinput():
#     global kill_flag
#     print('ehi?')
#     choice = input("Want to kill?")
#     if choice == '':
#         kill_flag = True
#     else:
#         return 0
#     return 1

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    # kill_flag = False
    # t = threading.Thread(target=joinThread(ACCEPT_THREAD))
    # t.start()
    # th2 = threading.Thread(target=askinput)
    # th2.start()

    # t.join()
    # th2.join()
    # while askinput():
    #     pass
    # exit_flag = input('Want to end?')
    # if exit_flag: ACCEPT_THREAD.stop()
    # ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    # ACCEPT_THREAD.start()
    # ACCEPT_THREAD.join()
    #   STA QUI FINCHè
    






