# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:44:18 2024

@author: neeb-meister
"""

from .ChessPiece import ChessPiece

class pawn(ChessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "pawn"
        self.collision = True
    def moveOptions(self,full_options=False,board=None):
        if board == None:
            board = self.board
        mod = self.fwd
        self.move_options = []
        dir0 = []
        dir1 = []
        dir2 = []
        dir3 = []
        dir4 = []
        if type(self.get_rel_space([1*mod,0],board)) == str:
            dir0.append([1*mod,0])
            if self.has_not_moved_yet:
                if type(self.get_rel_space([2*mod,0],board)) == str:
                    dir0.append([2*mod,0])
        dir1.append([1*mod,1])
        dir2.append([1*mod,-1]) 
        self.move_options.append(dir0)
        self.move_options.append(dir1)
        self.move_options.append(dir2)
        self.move_options.append(dir3)
        self.move_options.append(dir4)
        return self.move_options