# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:59:13 2024

@author: neeb-meister
"""
# the goal of the module is to recieve user inputs and to display the current state
# of the board
class ChessTextUI:
    def __init__(self,chessboard):
        self.name = 'ChessTextUI'
        self.comment_stream = ''
        self.cb = chessboard
    # show :
    def show(self):
        #print the current board in text
        #may get upgraded to graphics later on
        def piece2emoji(piece):
            if piece.color == "white":
                if piece.type =="pawn":
                    return "♙"
                if piece.type =="rook":
                    return "♖"
                if piece.type =="knight":
                    return "♘"
                if piece.type =="bishop":
                    return "♗"
                if piece.type =="king":
                    return "♔"
                if piece.type =="queen":
                    return "♕"
            else:
                if piece.type =="pawn":
                    return "♟️"
                if piece.type =="rook":
                    return "♜"
                if piece.type =="knight":
                    return "♞"
                if piece.type =="bishop":
                    return "♝"
                if piece.type =="king":
                    return "♚"
                if piece.type =="queen":
                    return "♛"
                
        def space2space(space_str):
            return " "
        
        def listElement2str(list_element):
            if type(list_element) == str:
                return space2space(list_element)
            else:
                return piece2emoji(list_element)
        
        #for each row, print the list of stuff in it
        for a, i in enumerate(self.cb.mat):
            #generate a list to print
            board_str_output = []
            for b, n in enumerate(i):
                board_str_output.append(listElement2str(n))
            board_str_output.append(8+-1*a)
            printrow = ' '.join(str(char) for char in board_str_output)
            print(printrow)
        print('a b c d e f g h 0')
        return True
    
    # say : string
    # recieves a comment from the board, handles it IG
    def say(self,comment,fast=True):
        # self.comment_stream += '\n'
        # self.comment_stream += comment
        # if flush:
        #     print(self.comment_stream)
        #     self.comment_stream = ''
        if fast:
            print(comment)
            
    # getInput : string
    # issue a request to the player with prompt, pass result back to board
    def getInput(self,prompt):
        info = input(prompt)
        return info



















