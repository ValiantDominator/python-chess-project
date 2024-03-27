# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:58:21 2024

@author: neeb-meister

Logging module
"""
# the goal of this class is to create game logs and write them to the current directory
# is passed a pointer to the ChessBoard. when called, it writes to the log

from datetime import datetime
import json
import logging

class ChessLog:
    def __init__(self,chessboard):
        self.log = {}
        self.log_stream = ''
        self.chessboard = chessboard
        self.tn = 0
        self.current_piece_pointer = None
        self.piece_pointer_dict = {}
        self.algebraic_notation_log = {}
        
    def write(self,tidbit,flush=False):
        # self.logentry = tidbit
        self.log[self.tn] = tidbit
        self.piece_pointer_dict[self.tn] = self.current_piece_pointer
        self.log["last move"] = tidbit
        self.tn += 1
    
    def save(self):
        now = datetime.now()
        curtime = now.strftime("%Y-%m-%d %H-%M-%S")
        self.log_name = curtime+" chess log.txt"
        with open(self.log_name,"w") as f:
            json.dump(self.log,f)
    
    def reset(self):
        self.log = {}
        self.log_stream = ''
        # self.logentry = ''
        self.tn = 0
        
    # loop over dicts in order
    def log_to_algebraic_notation(self):
        
        # le epic loop
        for turn_num, log_entry in self.log.items():
            #don't process stuff we've already done
            if turn_num == 'last move':
                # print('skipping:',turn_num)
                continue
            
            if turn_num in self.algebraic_notation_log.keys():
                # print('skipping:',turn_num)
                continue
            
            piece_pointer = self.piece_pointer_dict.get(turn_num)
            # print(f'piece pointer: {piece_pointer}')
            # print(f'{turn_num},{self.piece_pointer_dict}')
            
            start_pos = log_entry[1]
            end_pos = log_entry[2]
            args = log_entry[3]
            
            move_string = self._algebraic_notation(piece_pointer, start_pos, end_pos, **args)
            
            # start populating the algebraic dict
            self.algebraic_notation_log[turn_num] = move_string 
    
    # Sees if multiple pieces can move to the same square.
    # Returns a prefix that clarifies the the move
    def _ambiguous_move_prefix(self,piece_pointer,end_pos_int):
        debug = False
        
        piece_type = piece_pointer.type
        piece_color = piece_pointer.color
        
        # round up relevant pos
        start_pos_int = piece_pointer.pos()
        start_pos_not = self.chessboard.utils.int2not(start_pos_int)
        
        # check for other pieces on the board (exclude pawns)
        list_of_piece_on_board = [xd for xd in self.chessboard.list_of_pieces if xd.in_play]
        list_of_same_type_pieces = [xd for xd in list_of_piece_on_board if xd.type == piece_type and xd.color == piece_color]
        # remove self from the list
        try: 
            list_of_same_type_pieces.remove(piece_pointer)
        except Exception as e:
            logging.exception("An error occured: %s",e)
        if debug:
            print()
            print(f'My name: {piece_pointer.name}')
            print(f'List of potential conflicts: {[piece.name for piece in list_of_same_type_pieces]}')
            print('checking for conflict')
            print('end_pos:',end_pos_int)
            print('start_pos:',start_pos_int)
        
        locations_of_conflicting_piece = []
        for piece in list_of_same_type_pieces:
            if debug:
                print(f'{piece.name}: {piece.validMoves()}')
            if end_pos_int in piece.validMoves():
                if debug:
                    print("conflict detected from: {piece.name}")
                locations_of_conflicting_piece.append(piece.pos())
        # now check each coord and see if it is ambiguous
        if debug:
            print(f'locations of conflicts:{locations_of_conflicting_piece}')
            print()
        y_coord_can_differentiate = False
        x_coord_can_differentiate = False
        if len(locations_of_conflicting_piece):
            for loc in locations_of_conflicting_piece:
                if loc[0] != start_pos_int[0]:
                    y_coord_can_differentiate = True
            for loc in locations_of_conflicting_piece:
                if loc[1] != start_pos_int[1]:
                    x_coord_can_differentiate = True
                
        # generate prefix
        self.prefix = ''
        if x_coord_can_differentiate:
            self.prefix += start_pos_not[0]
        if y_coord_can_differentiate:
            self.prefix += start_pos_not[1]
        # print('prefix:',self.prefix)
    
    # Recieves many arguments and returns a string that has the correct notation
    def _algebraic_notation(self,piece_pointer, start_pos, end_pos, **kwargs):
        # unpack keyword arguments
        promotion = kwargs.get('promotion')
        check = kwargs.get('check')
        checkmate = kwargs.get('checkmate')
        en_passant = kwargs.get('en_passant')
        take = kwargs.get('take')
        
        # set piece pointer to more convenient name, get emoji
        piece = piece_pointer
        piece_symbol = self._piece2emoji(piece)
        
        # start building notation
        notation = ''
        
        # start with piece emoji
        if piece.type == "pawn":
            pass
        else:
            notation += piece_symbol
        
        # add any disambiguiating information
        notation += self.prefix
        
        # add an x if it's a take
        if take:
            notation += 'x'
            
        # add landing square
        notation += end_pos
        
        # add # if checkmate
        if checkmate:
            notation += '#'
        # add + if check
        elif check:
            notation += '+'
            
        # add e.p. if en_passant
        if en_passant:
            notation += ' e.p.'
        
        # add =piece if promotion
        if promotion:
            notation += '='
            notation += self._piece2emoji(promotion,True)
        
        return notation
    
    def _piece2emoji(self,piece,manual=False):
        if manual:
            piece_color, piece_type = piece
        else:
            piece_color = piece.color
            piece_type = piece.type
        if piece_color == "white":
            if piece_type =="pawn":
                return "♙"
            if piece_type =="rook":
                return "♖"
            if piece_type =="knight":
                return "♘"
            if piece_type =="bishop":
                return "♗"
            if piece_type =="king":
                return "♔"
            if piece_type =="queen":
                return "♕"
        else:
            if piece_type =="pawn":
                return "♟️"
            if piece_type =="rook":
                return "♜"
            if piece_type =="knight":
                return "♞"
            if piece_type =="bishop":
                return "♝"
            if piece_type =="king":
                return "♚"
            if piece_type =="queen":
                return "♛"
        print(piece,manual)
        return