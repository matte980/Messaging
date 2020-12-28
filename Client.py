#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
            msg_list.see('end')
        except OSError:  # Possibly client has left the chat.
            break
        print('ciao')


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    msg_list.see('end')
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

#----Now comes the sockets part----
HOST = '84.222.52.81' #YOUR EXTERNAL IP HERE
PORT = 33000

# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)

top = tk.Tk()
top.title("Chatter")

#   CONTAINER (non si espande)
container = ttk.Frame(top)

#   CANVAS
canvas = tk.Canvas(container)

#   SCROLLBAR
scrollbar = ttk.Scrollbar(container, orient='vertical', command= canvas.yview)  # To navigate through past messages.
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

#   MESSAGE TO BE SENT
my_msg = tk.StringVar()
my_msg.set("")

#   FILLS WITH FAKE MSGS
for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

#   INITIALIZE CANVAS
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

#   PACK CONTAINER, CANVAS, SCROLLBAR
container.pack(expand = True, fill=tk.BOTH)
canvas.pack(side="left", expand=True, fill=tk.BOTH)
scrollbar.pack(side="right", fill="y")

#   MESSAGES LIST
msg_list = tk.Listbox(canvas, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#   TEXT FIELD AND SEND BUTTON
entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
# entry_field.grid(column=0, row=0)
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()
# send_button.grid(column=1, row=0) 



top.protocol("WM_DELETE_WINDOW", on_closing)


#   SOCKET PART
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # Starts GUI execution.