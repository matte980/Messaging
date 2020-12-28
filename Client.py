#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import time


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            scrollable_frame.config(state='normal')
            scrollable_frame.insert(tk.END, msg + '\n')
            scrollable_frame.see('end')
            scrollable_frame.config(state='disabled')
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    scrollable_frame.config(state='normal')
    client_socket.send(bytes(msg, "utf8"))
    scrollable_frame.see('end')
    scrollable_frame.config(state='disabled')
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()
    time.sleep(.3)

#----Now comes the sockets part----
HOST = '84.222.52.81' #YOUR EXTERNAL IP HERE
PORT = 33000

# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)

#   TOP WINDOW & GRID CONFIG
top = tk.Tk()
top.title("Chatter")

top.grid_rowconfigure(0, weight=1)
top.grid_rowconfigure(1, weight=0)
top.grid_columnconfigure(0, weight=1)

#   FRAMES & GRID CONFIG
UpFrame = tk.Frame(top, bg='red')
DownFrame = tk.Frame(top, bg='green')

UpFrame.grid(column=0, row=0, sticky='nsew')
DownFrame.grid(column=0, row=1, sticky='sew')

UpFrame.grid_columnconfigure(0, weight=1)
UpFrame.grid_rowconfigure(0, weight=1)
DownFrame.grid_columnconfigure((0,1), weight=1)

#   SCROLLABLE FRAME
scrollable_frame = scrolledtext.ScrolledText(UpFrame,
                                 wrap = tk.WORD, width=40, height=15,
                                 font = ("Times New Roman", 15)
                                 )
scrollable_frame.grid(column=0, row=0, sticky='nsew')
scrollable_frame.config(state='normal')

#   MESSAGE IN TEXT
my_msg = tk.StringVar()
my_msg.set("")

#   TEXT FIELD AND SEND BUTTON
entry_field = tk.Entry(DownFrame, textvariable=my_msg)
entry_field.bind("<Return>", send) # FUNCTION TO CALL WHEN CLICKED
entry_field.grid(row=0, column=0, sticky='nsew')

send_button = tk.Button(DownFrame, text="Send", command=send)
send_button.grid(row=0, column=1, sticky='nsew')

#   FILLS WITH FAKE TEXT IF NECESSARY
# for i in range(50):
#     msg = "Sample scrolling label\n"
#     scrollable_frame.insert(tk.END, msg)

top.protocol("WM_DELETE_WINDOW", on_closing)

#   SOCKET PART
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # Starts GUI execution.