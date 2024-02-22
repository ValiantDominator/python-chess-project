# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 09:25:24 2024

@author: neeb-meister
"""
# chess_v2.py

import piece_classes as p
import json
from datetime import datetime

class chessBoard:
    def __init__(self,board=[]):
        if board == []:
            eightxempty1 = ["white_space","black_space","white_space","black_space",
                   "white_space","black_space","white_space","black_space"]
            eightxempty2 = ["black_space","white_space","black_space","white_space",
                            "black_space","white_space","black_space","white_space"]
            eightxyempty = [list(eightxempty1),list(eightxempty2),list(eightxempty1),list(eightxempty2),
                    list(eightxempty1),list(eightxempty2),list(eightxempty1),list(eightxempty2)]
        else:
            eightxyempty = board
        self.game_running = False
        self.mat = eightxyempty
        self.top = "black"
        self.backup = []
        self.active_player = "white"
        self.en_passant_fuel = False
        self.log = {}
        self.log["last move"] = ["black","a8","a8"]
        self.tn = 0
        self.templog = None
        now = datetime.now()
        curtime = now.strftime("%Y-%m-%d %H-%M-%S")
        self.log_name = curtime+" chess log.txt"
        for i in eightxyempty:
            self.backup.append(list(i))
        
    # resetBoard :
    # resets self.mat to a copy of self.backup
    # resets the board
    def resetBoard(self):
        self.tn=0
        self.log={}
        self.en_passant_fuel = False
        self.mat = [list(row) for row in self.backup]
      
    # playerValidMoves : player -> list of moves
    # gets every move that a player has
    def playerValidMoves(self,player):
        valid_moves = []
        for row in self.mat:
            for space in row:
                if type(space) != str:
                    if space.color == player:
                        valid_moves.append(space.validMoves()) 
        moves = [i for c in valid_moves for i in c] 
        return moves   
    
    # checkmate : player -> bool
    # gets every move that a player has, and returns True if he has no moves
    def checkmate(self,player):
        moves = self.playerValidMoves(player)
        return len(moves) == 0
    
    # not2int : string -> [int,int]
    # takes a notation string "a8" and translates it to int index [0,0]
    def not2int(self,notation,col=15):
        #return in format provided
        if col == 15 and type(notation)==list:
            row = notation[1]
            column = notation[0]
            row = 8 - row
            column = ord(column)-97
            return [row,column]
        elif col ==15:
            notation = [c for c in notation]
            row = int(notation[1])
            column = notation[0]
            row = 8 - row
            column = ord(column)-97
            return [row,column]
        else:
            row = int(col)
            column = notation
            row = 8 - row
            column = ord(column)-97
            return [row,column]
    
    # int2not: [int,int] -> string
    # takes int index and translates it to notation
    # [7,7] -> "h1"
    def int2not(self,integer,col=15):
        #return in format provided
        if col == 15:
            row = integer[0]
            column = integer[1]
            column = chr(column+97)
            row = -row+8
            return column+str(row)
        else:
            column = col
            row = integer
            row = -row+8
            column = chr(column+97)
            return column,row
        
    # notq : string -> bool
    # returns True if the string is valid notation
    def notq(self,string):
        try:
            ints = self.not2int(string)
            if ints[0] in range(8) and ints[1] in range(8):
                return True
            return False
        except:
            return False
        
    # placePieces : color 
    # places pieces on the board
    # does not reset the board, will overwrite what's on there
    def placePieces(self,top="black"):
        self.top = top
        if len(self.mat) != 8:
             print("Error: Unable to inialize board /nThere are not 8 columns")
             return None
        for a, i in enumerate(self.mat):
            if len(i) != 8:
                print("Error: Unable to inialize board /nRow " + a + " is not length 8")
                return None
        board4piece = [row for row in self.mat]
        #Define which side white starts on (top or bottom)
        top = top
        if top == "white":
            bot = "black"
        else:
            bot = "white"
        try:
            #fill out the top of pieces
            #start by looping over the pawn row
            for i, space in enumerate(self.mat[1]):
                self.mat[1][i] = p.pawn((top+" pawn "+str(i)),i,1,top,self)
            #get the rooks
            self.mat[0][0] = p.rook((top+" rook "+str(0)),0,0,top,self)
            self.mat[0][7] = p.rook((top+" rook "+str(1)),7,0,top,self)
            #get the knights
            self.mat[0][1] = p.knight((top+" knight "+str(0)),1,0,top,self)
            self.mat[0][6] = p.knight((top+" knight "+str(1)),6,0,top,self)
            #get the bishops
            self.mat[0][2] = p.bishop((top+" bishop "+str(0)),2,0,top,self)
            self.mat[0][5] = p.bishop((top+" bishop "+str(1)),5,0,top,self)
            #fill the king and queen correctly
            #if color matches the space, put the queen there and the king on the other
            if self.mat[0][3] == (top+"_space"):
                #place queen on its color
                self.mat[0][3] = p.queen((top+" queen"),3,0,top,self)
                self.mat[0][4] = p.king((top+" king"),4,0,top,self)
            else: #other case where king goes first
                #place queen on its color
                self.mat[0][4] = p.queen((top+" queen"),4,0,top,self)
                self.mat[0][3] = p.king((top+" king"),3,0,top,self)
            
            #fill out the bottom of pieces
            #start by looping over the pawn row
            for i, space in enumerate(self.mat[6]):
                self.mat[6][i] = p.pawn((bot+" pawn "+str(i)),i,6,bot,self)
            #get the rooks
            self.mat[7][0] = p.rook((bot+" rook "+str(0)),0,7,bot,self)
            self.mat[7][7] = p.rook((bot+" rook "+str(1)),7,7,bot,self)
            #get the knights
            self.mat[7][1] = p.knight((bot+" knight "+str(0)),1,7,bot,self)
            self.mat[7][6] = p.knight((bot+" knight "+str(1)),6,7,bot,self)
            #get the bishops
            self.mat[7][2] = p.bishop((bot+" bishop "+str(0)),2,7,bot,self)
            self.mat[7][5] = p.bishop((bot+" bishop "+str(1)),5,7,bot,self)
            #fill the king and queen correctly
            #if color matches the space, put the queen there and the king on the other
            if self.mat[7][3] == (bot+"_space"):
                #place queen on its color
                self.mat[7][3] = p.queen((bot+" queen"),3,7,bot,self)
                self.mat[7][4] = p.king((bot+" king"),4,7,bot,self)
            else: #other case where king goes first
                #place queen on its color
                self.mat[7][4] = p.queen((bot+" queen"),4,7,bot,self)
                self.mat[7][3] = p.king((bot+" king"),3,7,bot,self)
            # loop over every piece and have it find forward
            for row in self.mat:
                for space in row:
                    if type(space) != str:
                        space.forward(top)    
        except:
            print("Error: Unknown error initilizing board")
    
    # printBoard :
    # prints the board to the console in emoji form
    def printBoard(self):
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
        for a, i in enumerate(self.mat):
            #generate a list to print
            board_str_output = []
            for b, n in enumerate(i):
                board_str_output.append(listElement2str(n))
            board_str_output.append(8+-1*a)
            print(board_str_output)
        print(['a','b','c','d','e','f','g','h',0])
        return True
            
    # select : pos, bool -> active_piece
    # given a pos and bool, may prompt, returns active_piece
    def select(self,pos,fast):
        if fast:
            row,column = self.not2int(pos)
        else:
            column = input("column: ")
            row = int(input("row: "))
            row,column = self.not2int(column,row)
        active_piece = self.mat[row][column]
        if type(active_piece) == str:
            active_piece = ""
            print("Empty space. Select a piece")
        else:
            if active_piece.color != self.active_player:
                print("you do not control",active_piece.name)
                print()
                active_piece = ""
            else:
                print("you selected:",active_piece.name)
                print()
        return active_piece
    
    # tryPromote : active_piece
    # checks to see if promotion is in order, then promotes pawn to whatever
    # player desires
    def tryPromote(self,pc):
        if pc.type == "pawn":
            if (pc.fwd==1 and pc.y_pos==7)or(pc.fwd==-1 and pc.y_pos==0):
                print(pc.color,"promote",pc.name,":")
                while True:
                    upgrade = input("upgrade to: ")
                    if upgrade.lower() == "queen":
                        self.mat[pc.y_pos][pc.x_pos] = p.queen(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        break
                    elif upgrade.lower() == "rook":
                        self.mat[pc.y_pos][pc.x_pos] = p.rook(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        break
                    elif upgrade.lower() == "bishop":
                        self.mat[pc.y_pos][pc.x_pos] = p.bishop(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        break
                    elif upgrade.lower() == "knight":
                        self.mat[pc.y_pos][pc.x_pos] = p.knight(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        break
                    else:
                        print("invalid input:",upgrade)
    
    # move : active_piece, pos, bool :
    # moves selected piece to pos
    def move(self,active_piece,pos,fast):
        if active_piece == "":
                print("No piece selected")
        else:
            if fast:
                row,column = self.not2int(pos)
            else:
                column = input("column: ")
                row = int(input("row: "))
                row,column = self.not2int(column,row)
            print(f"you selected to move {active_piece.name} to {self.int2not([row,column])}")
            if [row,column] in active_piece.validMoves():
                log2 = active_piece.pos()
                taken = active_piece.move(row,column,self.mat)
                if type(taken) == str:
                    print(active_piece.name,"moved to",[row,column])
                else:
                    print(active_piece.name,"moved to",[row,column])
                    print("and took",taken.name)
                    print()
                # log entry : player, piece, move
                logentry = [self.active_player, self.int2not(log2),self.int2not([row,column])]
                if self.templog != None:
                    logentry = [self.active_player, self.templog, "z26"]
                    self.templog = None
                self.log[self.tn] = logentry
                self.log["last move"] = logentry
                self.tryPromote(active_piece)
                self.switchActivePlayer()
                self.tn += 1
                if self.checkmate(self.active_player):
                    self.printBoard()
                    self.switchActivePlayer()
                    print("CHECKMATE!",self.active_player,"WINS")
                    return True
            else:
                print("! invalid move !")
                print()
        self.printBoard()
        print(self.active_player,"to move")
        return False
            
    # switchActivePlayer : color -> color
    # returns white if black, black if white
    def switchActivePlayer(self):
        if self.active_player == "white":
            self.active_player = "black"
        else:
            self.active_player = "white"
        return True
    
    # play : color, bool 
    # creates an interactive window in the console to play the game
    def play(self,playertwocolor="black",playertwocomp=False):
        board = self.mat
        def name(space):
            if type(space) == str:
                return space
            else:
                return space.name
            
        if playertwocolor == "black":
            top_color = "black"
        else:
            top_color = "white"
        
        #gameplay loop
        active_piece = ""
        while True:
            #Start by prompting the user
            cmd = input("your input:    ")
            fast = False
            pos = []
            #one big try except for robustness
            # try:
                
            #proccess the input
            if len(cmd.split()) == 2:
                pos = cmd.split()[1]
                cmd = cmd.split()[0]
                fast = True
            
            
            # print -> prints board
            if cmd.lower() == "print":
                self.printBoard()
                print(self.active_player,"to move")
            
            # select -> selects a piece
            elif cmd.lower() == "select":
                active_piece = self.select(pos,fast)
                
            # move -> moves a piece (returns error if illegal)
            elif cmd.lower() == "move":
                if self.move(active_piece,pos,fast):
                    break
                
            # selected -> returns name of selected piece
            elif cmd.lower() == "selected":
                print(active_piece.name)
            
            # moves -> returns valid moves of selected piece
            elif cmd.lower() == "moves":
                tmpmoves = active_piece.validMoves()
                for a,i in enumerate(tmpmoves):
                    tmpmoves[a] = self.int2not(i)
                print(tmpmoves)
                
            # if cmd is notq and fast = True, then player passed select and move
            # together, run them together
            elif self.notq(cmd) and fast:
                if self.move(self.select(cmd,fast),pos,fast):
                    break
                
            elif cmd.lower() == "player":
                print(self.active_player)
                
            # help -> returns list of commands
            elif cmd.lower() == "help":
                print("print    : prints board")
                print("select   : prompts to select a piece")
                print("move     : prompts to move the selected piece")
                print("selected : returns name of selected piece")
                print("moves    : returns valid moves of selected piece")
                print("help     : shows this menu")
                print("quit     : exits the game")
                print("")
            
            # quit -> breaks the loop
            elif cmd.lower() == "quit":
                break
            
            # else return unknown command
            else:
                print("\nUnknown command: "+'"'+cmd+'"')
                print('type "help" to get a list of commands')
                
            # last step is to write the log file
            with open(self.log_name,"w") as f:
                json.dump(self.log,f)
            
            # except:
            #     print("Error")
            
            
            
if __name__ == '__main__':
    bod = chessBoard()
    bod.placePieces()
    bod.printBoard()
    bod.play()
            