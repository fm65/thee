import tkinter as tk
import src.config


class StatusBar(tk.Canvas):
    def __init__(self, master, bg, *args, **kwargs):
        super().__init__(master, highlightthickness=0, *args, **kwargs)
        self.master = master
        self.bg = bg
        self.label  = tk.Label(self,
        font=(src.config.font['statusbar']['family'], 
        src.config.font['statusbar']['size']),
        background=src.config.color['statusbarbg'],
        foreground=src.config.color['foreground'])
        self.label.pack(fill="x")

    def set(self, format, *args):
        self.label.config(text = format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()