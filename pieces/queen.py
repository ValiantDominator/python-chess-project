# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:49:06 2024

@author: neeb-meister
"""

from .ChessPiece import ChessPiece

class queen(ChessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[],utils=None):
        super().__init__(name, x, y, color,board,utils)
        self.type = "queen"
        self.collision = True
    def moveOptions(self,full_options=False,board=None):
        if board == None:
            board = self.board
        self.move_options = []
        dir0 = []
        dir1 = []
        dir2 = []
        dir3 = []
        dir4 = []
        dir5 = []
        dir6 = []
        dir7 = []
        for i in range(1,8):
            dir0.append([i,i])
            dir1.append([-i,i])
            dir2.append([i,-i])
            dir3.append([-i,-i])
            dir4.append([i,0])
            dir5.append([-i,0])
            dir6.append([0,i])
            dir7.append([0,-i])
        self.move_options.append(dir0)
        self.move_options.append(dir1)
        self.move_options.append(dir2)
        self.move_options.append(dir3) 
        self.move_options.append(dir4)
        self.move_options.append(dir5)
        self.move_options.append(dir6)
        self.move_options.append(dir7) 
        return self.move_options