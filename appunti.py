import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

top = tk.Tk()

#   GRID CONFIG
top.grid_rowconfigure(0, weight=1)
top.grid_rowconfigure(1, weight=0)
top.grid_columnconfigure(0, weight=1)

#   FRAMES
UpFrame = tk.Frame(top, bg='red')
DownFrame = tk.Frame(top, bg='green')

UpFrame.grid(column=0, row=0, sticky='nsew')
DownFrame.grid(column=0, row=1, sticky='sew')

UpFrame.grid_columnconfigure(0, weight=1)
UpFrame.grid_rowconfigure(0, weight=1)

DownFrame.grid_columnconfigure((0,1), weight=1)

#   SCROLLABLE FRAME
scrollable_frame = scrolledtext.ScrolledText(UpFrame,
                                 wrap = tk.WORD, font = ("Times New Roman", 15)
                                 )
scrollable_frame.grid(column=0, row=0, sticky='nsew')

#   TEXT
my_msg = tk.StringVar()
my_msg.set("")

#   TEXT FIELD AND SEND BUTTON
entry_field = tk.Entry(DownFrame, textvariable=my_msg)
entry_field.grid(row=0, column=0, sticky='nsew')
send_button = tk.Button(DownFrame, text="Send")
send_button.grid(row=0, column=1, sticky='nsew')

tk.mainloop()