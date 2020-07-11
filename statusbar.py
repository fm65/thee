import tkinter as tk
import config


class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, anchor="w",
        font=(config.font['statusbar']['family'], 
        config.font['statusbar']['size']), 
        background=config.color['statusbarbg'],
        foreground=config.color['foreground'])
        self.label.pack(fill="x")

    def set(self, format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()