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
        self.game_log_text = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.game_log_text.config(height=15)
        self.game_log_text.pack(expand=True, fill='both')
        
        # Add console log
        self.console_log_text = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.console_log_text.config(height=10)
        self.console_log_text.pack(expand=True, fill='both')
        
        # Input Line
        self.entry = tk.Entry(self.right_frame)
        self.entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.entry.bind("<Return>", self.submit_message)
        self.entry.focus_set()
        
        # Stack boxes
        self.root.pack_propagate(False)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=4)
        self.right_frame.grid_rowconfigure(1, weight=3)
        self.right_frame.grid_rowconfigure(2, weight=1)
        
        # Bring in our chess board
        self.chess_board = ChessBoardGUI(self.left_frame,self)
        self.chess_board.pack(expand=True, fill='both')
        
    
    def stop_game(self,winning_player):
        self.chess_board.stop_game(winning_player)
    
    
    def startGUI(self):
        # End, start main loop
        self.chess_board.render_pieces()
        self.root.mainloop()
        
    def setChessMain(self,chessmain):
        # Set chessmodule pointer
        self.chessmain = chessmain
        # print("successfully initialized aa")
        
    
    def submit_message(self,event):
        message = self.entry.get()
        self.chessmain.uiInput(message)
        self.console_log_text.config(state=tk.NORMAL)
        self.console_log_text.insert(tk.END, '\n' + message)
        self.console_log_text.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)
        self.console_log_text.see(tk.END)
        
    def update_graphics(self):
        self.chess_board.render_pieces()
        
    def UIinput(self,input_from_main):
        if input_from_main == 'update':
            self.update_graphics()
        
if __name__ == '__main__':
    MainGUI()