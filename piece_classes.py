# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 09:27:57 2024

@author: neeb-meister
"""
# piece_classes.py

class chessPiece:
    def __init__(self,name,x,y,color,chessboard):
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
        print("Couldn't find piece:  " + piece + "  on board")
        return " "
    
    # forward : top 
    # input top color to set what direction forward is
    # used to determine which way pawns move
    def forward(self,top):
        if self.color != top:
            self.fwd = -1
        else:
            self.fwd = 1
            
    # get_rel_space : [int, int] -> space (piece or str)
    # given relative coordinates, return the pointer to the desired space
    # translate a relative move to the real move
    def get_rel_space(self,coords):
        row_delta = coords[0]
        column_delta = coords[1]
        row_cur = self.y_pos
        column_cur = self.x_pos
        row_new = row_cur+row_delta
        column_new = column_cur+column_delta
        if not((row_new in range(8)) and (column_new in range(8))):
            return " "
        return self.board[row_new][column_new]
    
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
        relative_options = self.moveOptions(full_options)
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
        my_king = self.getPiece(self.color+" king",game_board)
        return self.spaceTakeable(game_board,player,my_king.pos(),full_options)
    
    # validMoves : () -> list_of_valid_moves
    # takes its own move options, its own board, and checks
    # each remaining move from primitivePossibilities and sees
    # if that simulated move puts its king in check
    def validMoves(self):
        moves = self.primitivePossibilities(self.board,True)
        is_king = self.type == "king"
        if is_king:
            selfinitx = self.x_pos
            selfinity = self.y_pos
            selfmovestorage = self.has_not_moved_yet
        for move in list(moves):
            temporary_board = [list(rows) for rows in self.board]
            self.move(move[0],move[1],temporary_board,is_king,False)
            last_move = self.chessboard.log["last move"]
            loc = self.chessboard.not2int(last_move[2])
            var1 = self.type == "pawn"
            var2 = type(self.board[move[0]][move[1]]) == str and self.x_pos!=move[1]
            var3 = [move[0]-self.fwd,move[1]] == loc and self.chessboard.en_passant_fuel
            var4 = not var3
            
            if self.inCheck(temporary_board,self.color,False):
                moves.remove(move)
                
            #the case where there's nothing to take on diag and it's not enpassant
            elif var1 and var2 and var4: 
                moves.remove(move)
        if is_king:
            self.has_not_moved_yet = selfmovestorage
            self.y_pos = selfinity
            self.x_pos = selfinitx
        return moves
    
class pawn(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "pawn"
        self.collision = True
        #for now I'll add all possible options to the pieces
        #i'll make a generic function for collision rules on the 
        #chess piece class. i'll add en passant later
    def moveOptions(self,not_full_options=False):
        mod = self.fwd
        self.move_options = []
        dir0 = []
        dir1 = []
        dir2 = []
        dir3 = []
        dir4 = []
        if type(self.get_rel_space([1*mod,0])) == str:
            dir0.append([1*mod,0])
            if self.has_not_moved_yet:
                if type(self.get_rel_space([2*mod,0])) == str:
                    dir0.append([2*mod,0])
        dir1.append([1*mod,1])
        dir2.append([1*mod,-1]) 
        self.move_options.append(dir0)
        self.move_options.append(dir1)
        self.move_options.append(dir2)
        self.move_options.append(dir3)
        self.move_options.append(dir4)
        return self.move_options
            #en passant stuff would go here       

class rook(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "rook"
        self.collision = True
    def moveOptions(self,not_full_options=False):
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
    
class knight(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "knight"
        self.collision = False
    def moveOptions(self,not_full_options=False):
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
    
class bishop(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "bishop"
        self.collision = True
    def moveOptions(self,fnot_full_options=False):
        self.move_options = []     
        dir0 = []
        dir1 = []
        dir2 = []
        dir3 = []
        for i in range(1,8):
            dir0.append([i,i])
            dir1.append([-i,i])
            dir2.append([i,-i])
            dir3.append([-i,-i])
        self.move_options.append(dir0)
        self.move_options.append(dir1)
        self.move_options.append(dir2)
        self.move_options.append(dir3) 
        
        return self.move_options      
    
class king(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "king"
        self.collision = False
    def moveOptions(self,full_options=True):
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
            rook0 = self.getPiece(self.color+" rook 0", self.board)
            rook1 = self.getPiece(self.color+" rook 1", self.board)
            dir8 = []
            dir9 = []
            dir8.append(self.check_castle(rook0))
            dir9.append(self.check_castle(rook1))
            if type(dir8[0]) == list:
                self.move_options.append(dir8)
            if type(dir9[0]) == list:
                self.move_options.append(dir9)
        return self.move_options
    
    def check_castle(self,rook):
        if rook == " ":
            return False
        if rook.has_not_moved_yet:
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
            enemy_can_take = self.playerPrimPos(self.board,enemy_player,False)
            #remove 1, maybe 2 squares from checking
            if[row,col_r] in enemy_can_take:
                enemy_can_take.remove([row,col_r])
            if col_r == 0 and [row,col_r+1] in enemy_can_take:
                enemy_can_take.remove([row,col_r+1])
                
            #check that all 3 squares are not threatened
            if queen_side_castle:
                for i in range(col_k-2,col_k+1):
                    if [row,i] in enemy_can_take:
                        return False
            else:
                for i in range(col_k,col_k+3):
                    if [row,i] in enemy_can_take:
                        return False
            
            #check that the spaces between are empty
            for i in range(small+1,big):
                if type(self.board[row][i]) != str:
                    return False
            if queen_side_castle:
                return [0,-2]
            else:
                return [0,2]
        else:
            return False
        
           
class queen(chessPiece):
    def __init__(self, name, x=0, y=0, color="white",board=[]):
        super().__init__(name, x, y, color,board)
        self.type = "queen"
        self.collision = True
    def moveOptions(self,not_full_options=False):
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
      