#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Fidel R. Monteiro"
__copyright__  = "Copyright 2020, The Pynosso Project"
__credits__    = ["Adilson A. Capaia", "https://effbot.org/tkinterbook", "Tkinter GUI Programming by Example"]
__license__    = ""
__version__    = "1.0"
__maintainer__ = "Fidel R. Monteiro"
__email__      = "fidelrmonteiro@gmail.com"
__status__     = "Production"

#------------------------------------------------------------------------#

import os
import config
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from pathlib import Path
from tkinter import filedialog

from textarea import TextArea
from linenumbers import LineNumbers
from highlighter import Highlighter
from findwindow import FindWindow
from terminal import Terminal


THEECONST_TOP    = 20
THEECONST_MIDDLE = 40
THEECONST_BOTTOM = 20


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.editor_mode_buffer   = ""
        self.terminal_mode_buffer = ""

        self.thee_mode   = 0 # 0: welcome, 1: editor, 2: terminal, 3: help 
        self.count_text_changed = 0
        self.key_buffer    = []

        self.active_mode = tk.StringVar()
        self.file_name   = tk.StringVar(value='untitled')
        self.status      = tk.StringVar(value="unsaved")
        self.spaces      = tk.StringVar(value="Spaces: 4")
        self.line        = tk.StringVar(value="Line 0 ")
        self.column      = tk.StringVar(value="Column 0")
        self.emun_line   = tk.StringVar(value="1")

        self.foreground       = config.color['foreground']
        self.background       = config.color['background']
        self.text_foreground  = config.color['text_foreground']
        self.text_background  = config.color['text_background']
        self.insertbackground = config.color['insertbackground']

        #=================== WINDOW SETTING ==================#
        self.title('thee')
        self.grid()
        self.minsize(550, 40) # (width, height)
        self.winfo_screenwidth  = self.winfo_screenwidth()
        self.winfo_screenheight = self.winfo_screenheight()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.width = self.winfo_screenwidth/3
        self.height = self.winfo_screenheight/2
        #========================== END =========================#

        #======================= FRAME CREATION ======================#
        self.topFrame  = tk.Frame(self, 
                width  = self.width, 
                height = THEECONST_TOP, 
                background     = config.color['menubg'])
        self.middleFrame = tk.Frame(self, 
                width  = self.width - THEECONST_TOP, 
                height = self.height - THEECONST_MIDDLE,
                background     = self.background)
        self.bottomFrame = tk.Frame(self, 
                  width  = self.width, 
                  height = THEECONST_BOTTOM, 
                  background     = config.color['statusbarbg'])

        #self.topFrame.grid(   row=0, column=0,  sticky='nwe', columnspan=2)
        self.middleFrame.grid(row=1, column=1, sticky='wens')
        self.bottomFrame.grid(row=2, column=0,  sticky='nwe', columnspan=2)
        #================================= END ==============================#
   
        self.config_dir = os.path.join(str(Path.home()), '.thee')

        self.text_font_size = config.font['text']['size']
        self.text_font_family = config.font['text']['family']

        self.statusbar_font_size = config.font['statusbar']['size']
        self.statusbar_font_family = config.font['statusbar']['family']

        self.create_text_widget() # Entry point ==========#
        self.terminal = Terminal(self, self.text_area) # run terminal

        #========================== ADD MENUBAR ITEMS =======================#
        menu_items = ["Ctrl+e", "Ctrl+t", "Ctrl+<number>" , 
        			  "Ctrl+a", "Ctrl+x", "Ctrl+c", "Ctrl+v", "Ctrl+z", "Ctrl+y", 
        			  "Ctrl+n", "Ctrl+o", "Ctrl+s", "Ctrl+S", "Ctrl+h"]

        for i, v in enumerate(menu_items, 1):
            tk.Label(self.topFrame, text=v + " " , background=config.color['menubg'], 
            	foreground=self.foreground, padx=4, 
                font=('TkMenuFont', 10, 'bold')).grid(row=0, column=i)
        #============================== END =================================#

        #======================= ADD STATUSBAR ITEMS ========================#
        self.label1 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.file_name, width=6)
        self.label1.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.label2 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.status, width=10)
        self.label2.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.label3 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.active_mode, width=10)
        self.label3.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        self.label4 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.spaces, width=10)
        self.label4.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.label5 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.line)
        self.label5.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.label6 = tk.Label(self.bottomFrame, background=config.color['statusbarbg'],
        foreground=self.foreground,
        font=(self.statusbar_font_family, self.statusbar_font_size), padx=4, textvariable=self.column)
        self.label6.pack(fill=tk.X, side=tk.LEFT, expand=True)
        #================================ END ===============================#

        self.bind_events()

        self.open_file = ''

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_text_widget(self):
        self.text_area = TextArea(self.middleFrame, 
        bg=self.text_background, fg=self.text_foreground, undo=True,
        font=(self.text_font_family, self.text_font_size), relief=tk.FLAT, 
        insertbackground=self.insertbackground)
        self.text_area.grid(row=1, column=1, sticky='wens')
        self.text_area.config(highlightthickness = 0)
        self.text_area.focus_set()
        self.welcome(event=None)

    def editor_mode(self, event=None):
        self.active_mode.set("Editor")
        self.text_area.config(state=tk.NORMAL, tabs=4)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, self.editor_mode_buffer)
        self.highlighter = Highlighter(self.text_area)
        self.thee_mode = 1

        self.linenumbers = LineNumbers(self.text_area)
        self.linenumbers.grid(row=1, column=0,  sticky='nsw')
        self.linenumbers.config(bg=self.text_background,
        width=len(self.linenumbers.line_number)*10, highlightthickness=0)

    def terminal_mode(self, event=None):
        self.active_mode.set("Terminal")
        self.file_name.set("Python3")
        self.text_area.config(state=tk.NORMAL, tabs=4)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, self.terminal_mode_buffer)
        self.terminal.writeLoop()
        self.highlighter = Highlighter(self.text_area)
        self.thee_mode = 2

    def text_been_modified(self, event=None):
        flag = self.text_area.edit_modified()
        if flag: # prevent from getting called twice
            if self.thee_mode == 1 and self.count_text_changed > 1: # editor mode
                self.editor_mode_buffer = self.text_area.get(1.0,  tk.END+"-1c")
                self.status.set("unsaved")
                self.update_line_column()
                self.linenumbers.config(width=len(self.linenumbers.line_number)*10)
            elif self.thee_mode == 2 and self.count_text_changed > 1: # terminal mode
                self.terminal_mode_buffer = self.text_area.get(1.0,  tk.END+"-1c")
                self.linenumbers.config(width=len(self.linenumbers.line_number)*10)
            self.count_text_changed += 1
        #reset so this will be called on the next change
        self.text_area.edit_modified(False)

    def update_line_column(self, event=None):
        if self.thee_mode == 1:
            line, column = self.text_area.index(tk.INSERT).split('.')
            fline        = f"Line {line}"
            fcolumn      = f"Column {int(column) + 1}"
            self.line.set(fline)
            self.column.set(fcolumn)
            self.emun_line.set(line)
            self.line_numbers = int(line)

    def retrieve_selected_line(self, event=None):
    	if self.thee_mode == 1:
            self.current_line = self.text_area.get("1.0",'end').rstrip()
            if event.keysym.isnumeric():
                self.key_buffer.append(event.keysym)
                # check buffer after 500ms (0.5s)
                self.after(500, self.selected_line_action)

    def selected_line_action(self):
        if self.key_buffer:
            index = int(''.join(self.key_buffer)) - 1
            self.key_buffer.clear()
            self.selected_line = self.current_line.split('\n')[index]
            selected_str  = self.selected_line + "\n"
            # write selected code line(s) to the console in order to it running
            self.terminal.proc.stdin.write(selected_str.encode())
            self.terminal.proc.stdin.flush()
            self.terminal_mode()

    def close_window(self):
        if self.editor_mode_buffer and self.status.get() == "unsaved":
            if msg.askokcancel("Quit", "Would you like to save the data?"):
                self.file_save()
                self.terminal.alive = False
                self.terminal.destroy()
            else:
                self.terminal.alive = False
                self.terminal.destroy()
        else:
            self.terminal.alive = False
            self.terminal.destroy()

    def bind_events(self):
        self.focus_set()
        self.text_area.bind_all('<<Modified>>',    self.text_been_modified)
        self.bind_all('<Button-1>',     self.update_line_column)
        self.text_area.bind('<Return>',self.enter)

        self.bind_all('<Control-e>',    self.editor_mode)
        self.bind_all('<Control-t>',  self.terminal_mode)
        self.bind_all('<Control-Key>', self.retrieve_selected_line)
        self.bind('<Control-f>', self.show_find_window)

        self.bind('<Control-n>', self.file_new)
        self.bind('<Control-o>', self.file_open)
        self.bind('<Control-s>', self.file_save)
        self.bind('<Control-S>', self.file_save_as)

        self.bind('<Control-w>', self.welcome)
        self.bind('<Control-h>', self.help_about)


    def enter(self, event=None):
    	if self.thee_mode == 2:
            self.terminal.enter()

    def show_find_window(self, event=None):
        FindWindow(self.bottomFrame, self.text_area)

    def show_welcome_page(self):
        self.active_mode.set("welcome")
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        message = '''
   		\n\n\n\n\n\n
   				     THEE

   				  version 1.0

   		     THE simple python key bindings  Editor

   		      type   Ctrl-h 	for help information

   	    	by Fidel R. Monteiro <fidelrmonteiro@gmail.com>

   		\n\n\n\n\n    
   		     The Pynosso Project | Sat, Jun 26 2020 
   		'''
        self.text_area.insert(tk.END, message)
        self.text_area.config(state=tk.DISABLED) 
        self.thee_mode = 0

    def show_about_page(self):
        self.active_mode.set("help")
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        message = '''
                        HELP

        Mode Commands
            Ctrl+e : Text mode
            Ctrl+t : Terminal mode
            Ctrl+<number> : Run selected line in python console

        Editing Commands
            Ctrl+a : Select all text
            Ctrl+x : Cut selected text
            Ctrl+c : Copy selected text
            Ctrl+v : Paste cut/copied text
            Ctrl+z : Undo
            Ctrl+y : Redo

        File Commands
            Ctrl+o : Open file
            Ctrl+s : Save current content
            Ctrl+S : Save current content as <filename>
            Ctrl+p : Print current content
            Ctrl+n : Open new file

        General
            Ctrl+m : Change syntax highlighting
            Ctrl+g : Change colour scheme
            Ctrl+l : Change font
            Ctrl+h : Display this help window

        AUTHOR
                Written by Fidel R. Monteiro (fm65)
                Sat, Jun 26 2020

        thee version 1.0

        "simple is better than complex"
        '''
        self.text_area.insert(tk.END, message)
        self.text_area.config(state=tk.DISABLED) 
        self.thee_mode = 3


    def apply_colour_scheme(self, foreground, background, text_foreground, text_background):
        self.text_area.configure(fg=text_foreground, bg=text_background)
        self.background = background
        self.foreground = foreground
        for menu in self.all_menus:
            menu.configure(bg=self.background, fg=self.foreground)

    def update_font(self):
        #self.load_font_file(self.font_scheme_path)
        self.text_area.configure(font=(self.text_font_family, self.text_font_size))

    def create_config_directory_if_needed(self):
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

    # =========== Menu Functions ==============

    def file_new(self, event=None):
        """
        Ctrl+N
        """
        self.text_area.delete(1.0, tk.END)
        self.open_file = None
        self.linenumbers.force_update()

    def file_open(self, event=None):
        """
        Ctrl+O
        """
        self.editor_mode()
        file_to_open = filedialog.askopenfilename(
        filetypes=[('Python files', '*.py')], defaultextension='.py')
        if file_to_open:
            self.open_file = file_to_open
            self.file_name.set(self.open_file.split('/')[-1])

            self.text_area.display_file_contents(file_to_open)
            self.highlighter.force_highlight()
            self.linenumbers.force_update()

    def file_save(self, event=None):
        """
        Ctrl+s
        """
        current_file = self.open_file if self.open_file else None
        if not current_file:
            current_file = filedialog.asksaveasfilename()
            self.file_name.set(current_file.split('/')[-1])

        if current_file:
            contents = self.text_area.get(1.0, tk.END)
            with open(current_file, 'w') as file:
                file.write(contents)
                self.status.set("saved")

    def file_save_as(self, event=None):
    	"""
    	Ctrl+S
    	"""
    	new_file_name = filedialog.asksaveasfilename(
        	filetypes=[('Python files', '*.py')], defaultextension='.py',
        	confirmoverwrite=False)
    	self.file_name.set(new_file_name.split('/')[-1])
    	f = open(self.new_file_name, 'w')
    	f.write(self.get('1.0', 'end'))
    	f.close()
    	self.status.set("saved")

    def edit_cut(self, event=None):
        """
        Ctrl+X
        """
        self.text_area.event_generate("<Control-x>")
        self.linenumbers.force_update()

    def edit_paste(self, event=None):
        """
        Ctrl+V
        """
        self.text_area.event_generate("<Control-v>")
        self.linenumbers.force_update()
        self.highlighter.force_highlight()

    def edit_copy(self, event=None):
        """
        Ctrl+C
        """
        self.text_area.event_generate("<Control-c>")

    def edit_select_all(self, event=None):
        """
        Ctrl+A
        """
        self.text_area.event_generate("<Control-a>")

    def edit_find_and_replace(self, event=None):
        """
        Ctrl+F
        """
        self.show_find_window()

    def welcome(self, event=None):
        """
        Ctrl+W
        """
        self.show_welcome_page()

    def help_about(self, event=None):
        """
        Ctrl+H
        """
        self.show_about_page()


def main():
	app = MainWindow()
	app.mainloop()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

