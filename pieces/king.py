# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:47:58 2024

@author: neeb-meister
"""

from .ChessPiece import ChessPiece

class king(ChessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "king"
        self.collision = False
    def moveOptions(self,full_options=False,board=None):
        if board == None:
            board = self.chessboard.mat
        self.move_options = []
        self.move_options.append([[1,1]])
        self.move_options.append([[0,1]])
        self.move_options.append([[1,0]])
        self.move_options.append([[-1,-1]])
        self.move_options.append([[-1,1]])
        self.move_options.append([[1,-1]])
        self.move_options.append([[-1,0]])
        self.move_options.append([[0,-1]])
        if self.has_not_moved_yet and full_options:
            rook0 = self.getPiece(self.color+" rook 0", self.chessboard.mat)
            rook1 = self.getPiece(self.color+" rook 1", self.chessboard.mat)
            dir8 = []
            dir9 = []
            dir8.append(self.check_castle(rook0))
            dir9.append(self.check_castle(rook1))
            if type(dir8[0]) == list:
                self.move_options.append(dir8)
            #     print("rook0","can castle")
            # else:
            #     print("rook0",dir8)
            if type(dir9[0]) == list:
                self.move_options.append(dir9)
            #     print("rook1","can castle")
            # else:
            #     print("rook1",dir9)
        return self.move_options
    
    def check_castle(self,rook):
        if rook == None:
            return "rook is none"
        elif isinstance(rook,str):
            return "rook does not exist"
        else:
            if self.color == "white":
                enemy_player = "black"
            else:
                enemy_player ="white"
            row = rook.y_pos
            col_k = self.x_pos
            col_r = rook.x_pos
            small = min([col_r,col_k])
            big = max([col_r,col_k])
            if col_r == 0:
                queen_side_castle = True
            else:
                queen_side_castle = False
            enemy_can_take = self.playerPrimPos(self.chessboard.mat,enemy_player,False)
            #remove 1, maybe 2 squares from checking
            if[row,col_r] in enemy_can_take:
                enemy_can_take.remove([row,col_r])
            if col_r == 0 and [row,col_r+1] in enemy_can_take:
                enemy_can_take.remove([row,col_r+1])
                
            #check that all 3 squares are not threatened
            if queen_side_castle:
                for i in range(col_k-2,col_k+1):
                    if [row,i] in enemy_can_take:
                        return "spaces threatened"
            else:
                for i in range(col_k,col_k+3):
                    if [row,i] in enemy_can_take:
                        return "spaces threatened"
            
            #check that the spaces between are empty
            for i in range(small+1,big):
                if type(self.chessboard.mat[row][i]) != str:
                    return "spaces clogged"
            if queen_side_castle:
                return [0,-2]
            return [0,2]
        return "idk even know"