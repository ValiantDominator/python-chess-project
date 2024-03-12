# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:43:23 2024

@author: neeb-meister
"""
import logging

class ChessPiece:
    def __init__(self,name,x,y,color,chessboard,utils):
        self.name = name
        self.is_chess_piece = True
        self.color = color
        self.x_pos = x
        self.y_pos = y
        self.in_play = True
        self.has_not_moved_yet = True
        self.fwd = 1
        self.chessboard = chessboard
        self.board = [row for row in chessboard.mat]
    
    # changeColor : color
    # obsolete function to change color
    def changeColor(self,color):
        self.color=color
        
    # taken :
    # sets in play to false to signify the piece has been taken
    def taken(self):
        self.in_play = False
        
    # pos : prt -> [y,x]
    # automatically doesn't print to console
    # return a list of row, column
    def pos(self,prt=False):
        if prt:
            print(str([self.y_pos,self.x_pos]))
        return [self.y_pos,self.x_pos]
    
    # getPiece : name, board -> piece
    # input a piece name and the board to search
    # return the instance of the piece
    def getPiece(self,piece,mat):
        for row in mat:
            for space in row:
                if type(space) != str:
                    if space.name == piece:
                        return space
        print("Couldn't find piece:  '" + piece + "'  on board")
        print("Calling piece:",self.name)
    
    # initialize : top 
    # input top color to set what direction forward is
    # used to determine which way pawns move
    # also give every piece a pointer to its own king
    def initialize(self,top):
        if self.color != top:
            self.fwd = -1
        else:
            self.fwd = 1
        self.my_king = self.getPiece(self.color+" king",self.board)
        
            
    # get_rel_space : [int, int] -> space (piece or str)
    # given relative coordinates, return the pointer to the desired space
    # translate a relative move to the real move
    def get_rel_space(self,coords,board = None):
        if board == None:
            board = self.board
        row_delta = coords[0]
        column_delta = coords[1]
        row_cur = self.y_pos
        column_cur = self.x_pos
        row_new = row_cur+row_delta
        column_new = column_cur+column_delta
        if not((row_new in range(8)) and (column_new in range(8))):
            return " "
        return board[row_new][column_new]
    
    # get_rel_coords : [int, int] -> [row, column]
    # given a relative move, adds current pos to return position
    def get_rel_coords(self,coords):
        # print(self.name," coords: ", coords)
        row_delta = coords[0]
        column_delta = coords[1]
        row_cur = self.y_pos
        column_cur = self.x_pos
        row_new = row_cur+row_delta
        column_new = column_cur+column_delta
        return [row_new,column_new]
        
    # move : row, column, board, bool -> space
    # given row, column, and board, move this piece to that space
    # returns old space
    # if bool is False, this piece does not update any of its info
    def move(self,row,column,mat,real_move=True,bonus_real_move=True):
        #define pointers for the old space and the new space
        new_space = mat[row][column]
        old_column = self.x_pos
        old_row = self.y_pos
        
        # if real_move:
        #     print("is this code running twice?")
        #     print('self.name:',self.name)
        #     print('row:',row)
        #     print('column:',column)
        #     print('real_move:',real_move)
        #     print()
            
        # check for en passant
        # remove the corresponding pawn
        if self.type == "pawn" and type(new_space) == str and old_column!=column:
            new_space = mat[row-self.fwd][column]
            mat[row-self.fwd][column] = " "
        
        # check for castle
        # move the corresponding rook
        if (self.type == "king" and abs(old_column-column) > 1) and (real_move and bonus_real_move):
            print("Castling done by:",self.name)
            if column == 2: #left castle
                rook = mat[row][0]
                rook.move(row,3,mat)
                self.chessboard.templog = "0 0 0"
            if column == 6: #right castle
                rook = mat[row][7]
                rook.move(row,5,mat)
                self.chessboard.templog = "0 0"
        
        # adding en_passant fuel if a pawn moved 2 spaces
        if (self.type == "pawn" and abs(old_row-row) == 2) and (real_move and bonus_real_move):
            self.chessboard.en_passant_fuel = True
        elif (real_move and bonus_real_move):
            self.chessboard.en_passant_fuel = False
            
        #change position data on this piece
        if real_move:
            self.x_pos = column
            self.y_pos = row
            self.has_not_moved_yet = False
                #if landed on a piece, take that piece
            if type(new_space) != str:
                new_space.taken()
        
        #put our piece at the new location, erase the old
        mat[old_row][old_column] = " "
        mat[row][column] = self
        
        #return the square we landed on, might be useful
        return new_space
    
    # actualizeOptions : list_of_relative_options -> list_of_real_options
    # take a list of relative options and returns a list of actual options
    def actualizeOptions(self,list_of_options):
        for seq, list_of_moves in enumerate(list_of_options):
            for spc, move in enumerate(list_of_moves):
                list_of_options[seq][spc] = self.get_rel_coords(move)
        return list_of_options
    
    # shaveDownOutOfBounds : list_of_real_options -> list_of_real_options
    # takes a list of real options and removes ones that are out of bounds
    def shaveDownOutOfBounds(self,list_of_options):
        for seq in list_of_options:
            for space in list(seq):
                my_bool = space[0] in range(8) and space[1] in range(8)
                if not my_bool:
                    seq.remove(space)
        return list_of_options
    
    # collisionCheck : list_of_real_options, game_board -> list_of_real_options
    # takes a list of options and a game board, and removes every option
    # after a collision
    def collisionCheck(self,list_of_options,game_board):
        for seq in list_of_options:
            start_deleting = False
            for space in list(seq):
                if type(game_board[space[0]][space[1]]) != str and start_deleting == False:
                    start_deleting = True
                    if game_board[space[0]][space[1]].color != self.color:
                        seq.append(space)
                if start_deleting:
                    seq.remove(space)
        return list_of_options
    
    # primitivePossibilities : game_board -> list_of_cond_options
    # takes itself and a game board, and returns a list of move options that 
    # does not include testing for check
    def primitivePossibilities(self,game_board,full_options=False):
        relative_options = self.moveOptions(full_options,game_board)
        real_options = self.actualizeOptions(relative_options)
        real_options = self.shaveDownOutOfBounds(real_options)
        real_options = self.collisionCheck(real_options, game_board)
        real_options = [option for direction in real_options for option in direction]
        return real_options
    
    # playerPrimPos : game_board, player -> list_of_cond_options
    # takes itself, a game board, and a player, and returns all 
    # primitive possiblities that player has
    def playerPrimPos(self,game_board,player,full_options=False):
        moves = []
        for row in game_board:
            for space in row:
                if type(space) != str:
                    if space.color == player:
                        move = space.primitivePossibilities(game_board,full_options)
                        moves.append(move)
        cmoves = [x for d in moves for x in d]
        return cmoves
    
    # spaceTakeable : game_board, player, space -> bool
    # takes a look at the game_board and a player, and returns true if the
    # enemy of that player can take that space
    def spaceTakeable(self,game_board,player,space,full_options=False):
        if player == "white":
            enemy_player = "black"
        else:
            enemy_player ="white"
        enemy_moves = self.playerPrimPos(game_board,enemy_player,full_options)
        answer = space in enemy_moves
        return answer
    
    # inCheck : game board, player -> bool
    # takes a look at a game_board and a player, and returns true if that player
    # is in check
    def inCheck(self,game_board,player,full_options=False):
        my_king = self.my_king
        return self.spaceTakeable(game_board,player,my_king.pos(),full_options)
    
    # validMoves : () -> list_of_valid_moves
    # takes its own move options, its own board, and checks
    # each remaining move from primitivePossibilities and sees
    # if that simulated move puts its king in check
    def validMoves(self):
        moves = self.primitivePossibilities(self.board,True)
        is_king = self.type == "king"
        selfinitx = self.x_pos
        selfinity = self.y_pos
        selfmovestorage = self.has_not_moved_yet
        for move in list(moves):
            temporary_board = [list(rows) for rows in self.board]
            self.move(move[0],move[1],temporary_board,is_king,False)
            if "last move" in self.chessboard.log:
                last_move = self.chessboard.log["last move"]
                loc = self.chessboard.utils.not2int(last_move[2])
            else:
                loc = None
                var1 = None
                var2 = None
                var3 = None
                var4 = None
                last_move = None

            var1 = self.type == "pawn"
            var2 = type(self.board[move[0]][move[1]]) == str and self.x_pos!=move[1]
            var3 = [move[0]-self.fwd,move[1]] == loc and self.chessboard.en_passant_fuel
            var4 = not var3
            
            if self.inCheck(temporary_board,self.color,False):
                moves.remove(move)
                
            #the case where there's nothing to take on diag and it's not enpassant
            elif var1 and var2 and var4: 
                moves.remove(move)
    
        self.has_not_moved_yet = selfmovestorage
        self.y_pos = selfinity
        self.x_pos = selfinitx
        return moves