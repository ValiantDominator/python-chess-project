# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:47:12 2024

@author: neeb-meister
"""

from .ChessPiece import ChessPiece

class knight(ChessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[],utils=None):
        super().__init__(name, x, y, color,board,utils)
        self.type = "knight"
        self.collision = False
    def moveOptions(self,full_options=False,board=None):
        if board == None:
            board = self.board
        self.move_options = []
        self.move_options.append([[1,2]])
        self.move_options.append([[1,-2]])
        self.move_options.append([[-1,2]])
        self.move_options.append([[-1,-2]])
        self.move_options.append([[2,1]])
        self.move_options.append([[2,-1]])
        self.move_options.append([[-2,1]])
        self.move_options.append([[-2,-1]])
        return self.move_options     