# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:45:29 2024

@author: neeb-meister
"""

from .ChessPiece import ChessPiece

class rook(ChessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[],utils=None):
        super().__init__(name, x, y, color,board,utils)
        self.type = "rook"
        self.collision = True
    def moveOptions(self,full_options=False,board=None):
        if board == None:
            board = self.board
        self.move_options = []  
        dir0 = []
        dir1 = []
        dir2 = []
        dir3 = []
        for i in range(1,8):
            dir0.append([i,0])
            dir1.append([-i,0])
            dir2.append([0,i])
            dir3.append([0,-i])
        self.move_options.append(dir0)
        self.move_options.append(dir1)
        self.move_options.append(dir2)
        self.move_options.append(dir3)
        return self.move_options       