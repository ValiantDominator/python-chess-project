# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 08:36:23 2024

@author: neeb-meister
"""

import tkinter as tk
from PIL import Image, ImageTk
from .chessframe import ChessBoardGUI

class MainGUI:
    def __init__(self):
        
        # Create root and title
        self.root = tk.Tk()
        self.root.title("PyChess")
        
        self.iconname = 'horsey.ico'
        self.root.iconbitmap(self.iconname)
        
        # Set default size of window
        self.root.geometry('800x600')
        
        # Create frames
        # left frame for chess board
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill='both')
        
        # right frame for log and console
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.LEFT, expand=True, fill='both')
        
        # Add game log
        self.game_log_text = Notation(self.right_frame,self)
        self.game_log_text.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # Add console log
        self.console_log_text = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.console_log_text.config(height=10)
        self.console_log_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # Input Line
        self.entry = tk.Entry(self.right_frame)
        self.entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.entry.bind("<Return>", self.submit_message)
        self.entry.focus_set()
        
        # Stack boxes
        self.root.pack_propagate(False)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=4)
        self.right_frame.grid_rowconfigure(1, weight=4)
        self.right_frame.grid_rowconfigure(2, weight=1)
        
        # Bring in our chess board
        self.chess_board = ChessBoardGUI(self.left_frame,self)
        self.chess_board.pack(expand=True, fill='both')
        
    
    def stop_game(self,winning_player):
        self.chess_board.stop_game(winning_player)
    
    
    def startGUI(self):
        # End, start main loop
        self.chess_board.render_pieces()
        self.game_log_text.postinit()
        self.root.mainloop()
        
    def setChessMain(self,chessmain):
        # Set chessmodule pointer
        self.chessmain = chessmain
        # print("successfully initialized aa")
        
    
    def submit_message(self,event):
        # get the message
        message = self.entry.get()
        
        # pass it to the board
        self.chessmain.uiInput(message)
        
        # add it to the console log
        self.add_text_to_console_log(message)
        
    def add_text_to_console_log(self,text):
        self.console_log_text.config(state=tk.NORMAL)
        self.console_log_text.insert(tk.END, '\n' + text)
        self.console_log_text.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)
        self.console_log_text.see(tk.END)
        
    def update_graphics(self):
        self.chess_board.render_pieces()
        self.game_log_text.delete_text()
        self.game_log_text.write_not()
        
    def UIinput(self,input_from_main,cmd=None):
        if input_from_main == 'update':
            self.update_graphics()
        if cmd == 'print':
            print('ran"')
            self.add_text_to_console_log(input_from_main)
        
        
class Notation(tk.Frame):
    def __init__(self,master,MainGUI):
        super().__init__(master)
        self.name = "notation frame"
        self.master = master
        self.maingui = MainGUI
        
        self.left_column = tk.Text(self,width=5,wrap=tk.WORD,state=tk.DISABLED,font=('Arial',10))
        self.left_column.grid(row=0,column=0,sticky='nsew')
        
        self.right_column = tk.Text(self,width=5,wrap=tk.WORD,state=tk.DISABLED,font=('Arial',10))
        self.right_column.grid(row=0,column=1,sticky='nsew')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
    
    def postinit(self):
        self.log = self.maingui.chessmain.board.chesslog
    
    def write_not(self):
        moves = self.log.algebraic_notation_log
        for move_num, move in moves.items():
            move_num+=1
            if move_num < 10:
                stuff_to_write = str(move_num)+' . '+move
            else:
                stuff_to_write = str(move_num)+'. '+move
            
            if move_num % 2 == 1:
                self.add_text(self.left_column, stuff_to_write)
            else:
                self.add_text(self.right_column, stuff_to_write)
        
    def add_text(self,column,text):
        column.configure(state=tk.NORMAL)
        column.insert("end", text + "\n")
        column.configure(state=tk.DISABLED)
        column.see("end") 
        
    def delete_text(self):
        self.left_column.configure(state=tk.NORMAL)
        self.left_column.delete(1.0, "end")
        self.left_column.configure(state=tk.DISABLED)
        self.right_column.configure(state=tk.NORMAL)
        self.right_column.delete(1.0, "end")
        self.right_column.configure(state=tk.DISABLED)
        
# class Menus(tk.Menu):
#     def __init__(self,master,MainGUI):
        