# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:58:42 2024

@author: neeb-meister

Board
"""

from pieces import Pieces as p
from utils import ChessUtils
from chesslogging import ChessLog
from ui import ChessTextUI
import logging
import sys
import copy

log_display = False

class ChessBoard:
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
        self.tn = 0
        for i in eightxyempty:
            self.backup.append(list(i))
        self.chesslog = ChessLog(self)
        self.ui = ChessTextUI(self)
        self.utils = ChessUtils()
        self.board_states = []
        self.log = {}
        self.templog = ''
    
    # weigh_self :
    # returns size of self
    def weigh_self(self):
        print("Size of object:", sys.getsizeof(self.mat), "bytes")
    
    # setUI : UI module
    # sets ui to given module
    def setChessMain(self,module):
        self.chessmain = module
        # print("successfully initialized")
    
    # resetBoard :
    # resets self.mat to a copy of self.backup
    # resets the board
    def resetBoard(self):
        self.tn=0
        self.chessLog.reset()
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
    def checkmate(self,player,reverse=False):
        if (player == "white") ^ reverse:
            player_to_check = "white"
        else:
            player_to_check = "black"
        moves = self.playerValidMoves(player_to_check)
        return len(moves) == 0
    
    # in_check : player -> bool
    # returns true if a player is in check rn
    def in_check(self,player,reverse=False):
        if (player == "white") ^ reverse:
            player_to_check = "white"
            enemy = "black"
        else:
            player_to_check = "black"
            enemy = "white"
        moves = self.playerValidMoves(enemy)
        packed_king = [piece for piece in self.list_of_pieces if piece.name == player_to_check+' king']
        king = packed_king[0]
        if king.pos() in moves:
            return True
        return False
        
    # placePieces : color 
    # places pieces on the board
    # does not reset the board, will overwrite what's on there
    def placePieces(self,top="black"):
        self.list_of_pieces = []
        utils = ChessUtils()
        self.top = top
        # if len(self.mat) != 8:
        #      print("Error: Unable to inialize board /nThere are not 8 columns")
        #      return None
        # for a, i in enumerate(self.mat):
        #     if len(i) != 8:
        #         print("Error: Unable to inialize board /nRow " + a + " is not length 8")
        #         return None
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
                self.mat[1][i] = p.pawn((top+" pawn "+str(i)),i,1,top,self,self.utils)
            #get the rooks
            self.mat[0][0] = p.rook((top+" rook "+str(0)),0,0,top,self,self.utils)
            self.mat[0][7] = p.rook((top+" rook "+str(1)),7,0,top,self,utils)
            #get the knights
            self.mat[0][1] = p.knight((top+" knight "+str(0)),1,0,top,self,utils)
            self.mat[0][6] = p.knight((top+" knight "+str(1)),6,0,top,self,utils)
            #get the bishops
            self.mat[0][2] = p.bishop((top+" bishop "+str(0)),2,0,top,self,utils)
            self.mat[0][5] = p.bishop((top+" bishop "+str(1)),5,0,top,self,utils)
            #fill the king and queen correctly
            #if color matches the space, put the queen there and the king on the other
            if self.mat[0][3] == (top+"_space"):
                #place queen on its color
                self.mat[0][3] = p.queen((top+" queen"),3,0,top,self,utils)
                self.mat[0][4] = p.king((top+" king"),4,0,top,self,utils)
            else: #other case where king goes first
                #place queen on its color
                self.mat[0][4] = p.queen((top+" queen"),4,0,top,self,utils)
                self.mat[0][3] = p.king((top+" king"),3,0,top,self,utils)
            
            #fill out the bottom of pieces
            #start by looping over the pawn row
            for i, space in enumerate(self.mat[6]):
                self.mat[6][i] = p.pawn((bot+" pawn "+str(i)),i,6,bot,self,utils)
            #get the rooks
            self.mat[7][0] = p.rook((bot+" rook "+str(0)),0,7,bot,self,utils)
            self.mat[7][7] = p.rook((bot+" rook "+str(1)),7,7,bot,self,utils)
            #get the knights
            self.mat[7][1] = p.knight((bot+" knight "+str(0)),1,7,bot,self,utils)
            self.mat[7][6] = p.knight((bot+" knight "+str(1)),6,7,bot,self,utils)
            #get the bishops
            self.mat[7][2] = p.bishop((bot+" bishop "+str(0)),2,7,bot,self,utils)
            self.mat[7][5] = p.bishop((bot+" bishop "+str(1)),5,7,bot,self,utils)
            #fill the king and queen correctly
            #if color matches the space, put the queen there and the king on the other
            if self.mat[7][3] == (bot+"_space"):
                #place queen on its color
                self.mat[7][3] = p.queen((bot+" queen"),3,7,bot,self,utils)
                self.mat[7][4] = p.king((bot+" king"),4,7,bot,self,utils)
            else: #other case where king goes first
                #place queen on its color
                self.mat[7][4] = p.queen((bot+" queen"),4,7,bot,self,utils)
                self.mat[7][3] = p.king((bot+" king"),3,7,bot,self,utils)
            # loop over every piece and have it find forward
            for row in self.mat:
                for space in row:
                    if type(space) != str:
                        space.initialize(top)
                        self.list_of_pieces.append(space)
            # print("board init yes")
        except Exception as e:
            # print("gang signs")
            logging.exception("An error occured: %s",e)

    # select : pos -> active_piece
    # given a pos and bool, may prompt, returns active_piece
    def select(self,pos):
        row,column = self.utils.not2int(pos)
        active_piece = self.mat[row][column]
        if type(active_piece) == str:
            active_piece = ""
            # print("Empty space. Select a piece")
        else:
            if active_piece.color != self.active_player:
                # print("you do not control",active_piece.name)
                # print()
                active_piece = ""
            # else:
                # print("you selected:",active_piece.name)
                # print()
        # print('selected:',active_piece)
        self.active_piece = active_piece
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
                        self.mat[pc.y_pos][pc.x_pos].my_king = pc.my_king
                        self.mat[pc.y_pos][pc.x_pos].fwd = pc.fwd
                        return self.mat[pc.y_pos][pc.x_pos]
                    elif upgrade.lower() == "rook":
                        self.mat[pc.y_pos][pc.x_pos] = p.rook(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        self.mat[pc.y_pos][pc.x_pos].my_king = pc.my_king
                        self.mat[pc.y_pos][pc.x_pos].fwd = pc.fwd
                        return self.mat[pc.y_pos][pc.x_pos]
                    elif upgrade.lower() == "bishop":
                        self.mat[pc.y_pos][pc.x_pos] = p.bishop(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        self.mat[pc.y_pos][pc.x_pos].my_king = pc.my_king
                        self.mat[pc.y_pos][pc.x_pos].fwd = pc.fwd
                        return self.mat[pc.y_pos][pc.x_pos]
                    elif upgrade.lower() == "knight":
                        self.mat[pc.y_pos][pc.x_pos] = p.knight(pc.name,pc.x_pos,pc.y_pos,pc.color,self)
                        self.mat[pc.y_pos][pc.x_pos].my_king = pc.my_king
                        self.mat[pc.y_pos][pc.x_pos].fwd = pc.fwd
                        return self.mat[pc.y_pos][pc.x_pos]
                    else:
                        print("invalid input:",upgrade)
        return None
    
    # move : active_piece, pos :
    # checks if a move is valid, then executes it
    def move(self,active_piece,pos):
        row,column = self.utils.not2int(pos)
        
        # check if move is valid
        valid = self.moveValid(active_piece,row,column)
        if not valid:
            print('invalid move')
            return False
        
        # then execture the move
        return self.moveExecute(active_piece,row,column)
        
    
    # moveValid : active_piece, row, column -> bool
    # checks if a move is valid before passing it to move function
    def moveValid(self,active_piece,row,column):
        # If there is no active piece
        if isinstance(active_piece,str):
            print('invalid move, is string')
            return False
        # If the move isn't valid
        if not [row,column] in active_piece.validMoves():
            return False
        
        return True
            
            
    # moveExecute : active_piece, row, column
    # executes a move. 
    def moveExecute(self,active_piece,row,column):
        # before the move executes, check the board state to see if a prefix
        # needs to be generated
        self.chesslog._ambiguous_move_prefix(active_piece, [row,column])
        
        # Execute the Move
        taken, en_passant = active_piece.move(row,column,self.mat)
        
        # outstream and processing taken for log
        outstream = {}
        if isinstance(taken,str):
            outstream['move']=[active_piece.name,"moved to",[row,column]]
            piece_taken = False
        else:
            outstream['move']=[active_piece.name,"moved to",[row,column],"and took",taken.name]
            piece_taken = True
        
        # notate if a piece was taken
        
        # try to promote piece
        promotion = self.tryPromote(active_piece)
        if promotion:
            promote = (promotion.color,promotion.type)
        else:
            promote = None
        
        # see if it puts enemy in check
        check = self.in_check(self.active_player,True)
        
        # see if it is checkmate
        checkmate = self.checkmate(self.active_player,True)
        
        # prepare extra arguments
        args = {'promotion':promote,'check':check,'checkmate':checkmate,'en_passant':en_passant,'take':piece_taken}
        
        # log entry : player, piece, move, extra_arg
        log2 = active_piece.pos()
        logentry = [self.active_player, self.utils.int2not(log2),self.utils.int2not([row,column]),args]
        
        # send piece pointer to chess log as well, this helps with algebraic notation
        self.chesslog.current_piece_pointer = active_piece
        
        # send log entry to chess log
        self.chesslog.write(logentry)

        # add to local log for use in en-passant logic
        self.log[self.tn] = logentry
        self.log["last move"] = logentry
        
        # switch the active player, increment turn number
        self.switchActivePlayer()
        self.tn += 1
        
        # cook the algebraic notation
        self.chesslog.log_to_algebraic_notation()
        
        # print to log
        # print('move executed')
        
        # if checkmate, return True for game over
        if checkmate:
            self.ui.show()
            self.switchActivePlayer()
            print("CHECKMATE!",self.active_player,"WINS")
            return True
    
    # switchActivePlayer : color -> color
    # returns white if black, black if white
    def switchActivePlayer(self):
        if self.active_player == "white":
            self.active_player = "black"
        else:
            self.active_player = "white"

    # readLog : 
    # prompts user to select game, reads game to a file
    def readLog(self):
        self.playing = False
        data = ChessUtils.open_txt_file()
        del data["last move"]
        n = 0
        largest_key = max(int(key) for key in data.keys())
        print(f"largest_key {largest_key}")
        last_turn_num = largest_key
        while n < int(last_turn_num):
            m = str(n)
            if data[m][2] == None or data[m][2] == 'z26':
                self.handleInput(data[m][1])
            else:
                self.handleInput(data[m][1]+' '+data[m][2])
            print()
            print(f"Game state at turn {n+1}, {data[m][0]}'s move")
            self.ui.show()
            print()
            print("'break' to continue game from this point")
            print("'back' to go back 1 move")
            print(" any input to continue")
            cmd = input(' >   ')
            cmd = cmd.lower()
            if cmd == "break":
                break
            elif cmd == "back":
                n += -1
            else:
                n += 1
        if cmd == "break":
            self.active_player = data[str(n+1)][0]
            self.play()
    
    # gameHelp : 
    # helper fucntion for handleInput, prints the help blurb
    def gameHelp(self):
        print("print    : prints board")
        print("select   : prompts to select a piece")
        print("move     : prompts to move the selected piece")
        print("selected : returns name of selected piece")
        print("moves    : returns valid moves of selected piece")
        print("help     : shows this menu")
        print("quit     : exits the game")
        print("")
        return None
    
    # handleInput : str 
    # helper function for play(), given input it handles what to do
    def handleInput(self,cmd):
        # write the log file
        # print("cmd:",cmd)
        if cmd == "0 0" and self.active_player == "white":
            cmd = "e1 g1"
        elif cmd == "0 0" and self.active_player == "black":
            cmd = "e8 g8"
        elif cmd == "0 0 0" and self.active_player == "white":
            cmd = "e1 c1"
        elif cmd == "0 0 0" and self.active_player == "black":
            cmd = "e8 c8"
        
        # check for fast move
        fast = False
        pos = []
        if len(cmd.split()) == 2:
            pos = cmd.split()[1]
            cmd = cmd.split()[0]
            if self.utils.notq(pos) and self.utils.notq(cmd):
                fast = True
        
        # print -> prints board
        if cmd.lower() == "print":
            self.ui.show()
            # print(self.active_player,"to move")
            return False
        
        # select -> selects a piece
        elif cmd.lower() == "select":
            self.select(pos)
            return False
            
        # move -> moves a piece (returns error if illegal)
        elif cmd.lower() == "move":
            return self.move(self.active_piece,pos)
            
        # selected -> returns name of selected piece
        elif cmd.lower() == "selected":
            # print(self.active_piece.name)
            return False
        
        # moves -> returns valid moves of selected piece
        elif cmd.lower() == "moves":
            tmpmoves = self.active_piece.validMoves()
            for a,i in enumerate(tmpmoves):
                tmpmoves[a] = self.utils.int2not(i)
            # print(tmpmoves)
            return False
            
        # if fast, run select and move together
        elif fast:
            return self.move(self.select(cmd),pos)
        
        # player
        elif cmd.lower() == "player":
            # print(self.active_player)
            return False
        
        # help -> returns list of commands
        elif cmd.lower() == "help":
            self.gameHelp()
            return False
        
        # quit -> breaks the loop
        elif cmd.lower() == "quit":
            return True
        
        # load -> loads game from log
        elif cmd.lower() == "load":
            self.readLog()
            return False
        
        # else return unknown command
        else:
            # print("\nUnknown command: "+'"'+cmd+'"')
            # print('type "help" to get a list of commands')
            return False
            
    # play : color, bool 
    # creates an interactive window in the console to play the game
    def play(self,playertwocolor="black",playertwocomp=False):
        self.active_piece = ""
        self.playing = True
        while True:
            cmd = input("your input:    ")
            try:
                stop = self.handleInput(cmd)
                if stop:
                    break
            except Exception as e:
                logging.exception("An error occured: %s",e)
                
    # chessBoardInput : input_from_main
    def chessBoardInput(self,input_from_main):
        game_over = self.handleInput(input_from_main)
        if game_over:
            self.chesslog.save()
            self.chessmain.ui.stop_game(self.active_player)
            self.chessmain.ui.chess_board.render_pieces()
        else:
            # do stuff
            pass
        # call output function
        self.chessBoardOutput()
        
    def chessBoardOutput(self,output_to_main=None):
        self.chessmain.chessBoardInput(output_to_main)
