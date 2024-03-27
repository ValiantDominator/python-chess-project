# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:57:48 2024

@author: neeb-meister

MAIN MODULE
"""
# the purpose of this module is to contain simple user config, and to run
# a working game of chess by running this script
from board import ChessBoard
from gui import maingui
import logging

# config variables



# ChessMain class
class ChessMain:
    def __init__(self,ChessBoard,UI):
        ChessBoard.setChessMain(self)
        UI.setChessMain(self)
        self.board = ChessBoard
        self.ui = UI
        
    def mainloop(self):
        self.ui.startGUI()
    
    def uiInput(self,input_from_ui):
        # pass input straight to board
        msg = input_from_ui.lower()
        if msg == 'xd':
            self.ui.chess_board.destroy_temp_graphics()
        elif msg == 'reset selection':
            self.ui.chess_board.render_pieces()
        elif msg == 'full log':
            print(self.board.log)
        elif msg == 'log':
            print(self.board.log['last move'])
        else: 
            self.chessBoardOutput(input_from_ui)
    
    def uiOutput(self,output_to_ui,cmd=None):
        self.ui.UIinput(output_to_ui,cmd)
    
    def chessBoardInput(self,input_from_chessboard):
        # do nothing
        if input_from_chessboard[0] == "print":
            self.uiOutput(input_from_chessboard[1],'print')
            
        else:
            self.uiOutput('update')
    
    def chessBoardOutput(self,output_to_chessboard):
        # pass straight to board
        if True:
            self.board.chessBoardInput(output_to_chessboard)
        
        

# Main Function
def main():
    board = ChessBoard()
    gui = maingui.MainGUI()
    chessmain = ChessMain(board,gui)
    chessmain.mainloop()

# if __name__ == '__main__':
#     main()

board = ChessBoard()
gui = maingui.MainGUI()
chessmain = ChessMain(board,gui)
board.placePieces()
chessmain.mainloop()