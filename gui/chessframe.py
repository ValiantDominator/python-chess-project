# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:08:04 2024

@author: neeb-meister
"""

import tkinter as tk
from PIL import Image, ImageTk
import time

# Create a class for the board
class ChessBoardGUI(tk.Frame):
    def __init__(self,master,MainGUI):
        super().__init__(master)
        self.master = master
        self.maingui = MainGUI
        
        # Fun variables
        self.board_number_of_rows = 8
        
        # Create the board
        self.create_board()
        
        # Bind
        self.bind("<Configure>", self.resize_board)
        
        # Move Handling Variables
        self.selected_square = ()
        self.ready_to_move = False
        self.game_over = False
    
    def create_board(self):
        self.squares = []
        self.colors = ['white', 'gray']
        for row in range(self.board_number_of_rows):
            row_squares = []
            for col in range(self.board_number_of_rows):
                # get grid color
                color = self.colors[(row + col) % 2]
                
                # create a square as a canvas filled with color
                square = BoardSquare(self, bg=color, highlightthickness=0)
                
                # place the square where it goes in the frame
                square.grid(row = row, column = col, sticky="nsew")
                
                # add a button on the square that waits to be clicked
                square.bind("<Button-1>", lambda event, row=row, col=col: self.square_clicked(row, col))
                square.bind("<Button-3>", self.reset_selection)
                # add the square to our temp row
                row_squares.append(square)
            # add the row to our squares list for storage
            self.squares.append(row_squares)
        
    def resize_board(self, event):
        width = event.width
        height = event.height
        size = min(width, height)
        square_size = size // self.board_number_of_rows
        
        for row in range(self.board_number_of_rows):
            for col in range (self.board_number_of_rows):
                self.squares[row][col].config(width=square_size, height=square_size)
                self.squares[row][col].resize_square()
                
    def square_clicked(self, row, col):
        if self.game_over:
            return None
        space = self.maingui.chessmain.board.mat[row][col]
        if isinstance(space,str):
            name = 'empty'
        else:
            name = space.name
        print(f"Square clicked: {row}, {col}  :  {name}")
        pos = (row, col)
        
        if self.ready_to_move:
            cmd = self.translate_positions_to_notation(self.selected_square,pos)
            self.maingui.chessmain.uiInput(cmd)
            self.reset_selection()
        
        if self.try_select(pos):
            self.render_pieces()
            self.add_move_decoration()
            self.ready_to_move = True
    
    def translate_positions_to_notation(self,pos1,pos2):
        row1,col1=pos1
        row2,col2=pos2
        str1 = self.maingui.chessmain.board.utils.int2not([row1,col1])
        str2 = self.maingui.chessmain.board.utils.int2not([row2,col2])
        return str1+' '+str2
    
    def reset_selection(self,event=None):
        self.ready_to_move = False
        self.selected_square = ()
        self.render_pieces()
        
    def add_move_decoration(self):
        valid_moves = self.valid_moves_for_selected_piece()
        for row in range(self.board_number_of_rows):
            for col in range (self.board_number_of_rows):
                if [row,col] in valid_moves:
                    self.squares[row][col].blue_dot_myself()
        
    def render_pieces(self):
        # print("rendering pieces")
        self.list_of_piece_graphics = []
        list_of_pieces = self.maingui.chessmain.board.mat
        for row in range(self.board_number_of_rows):
            for col in range (self.board_number_of_rows):
                square = self.squares[row][col]
                space = list_of_pieces[row][col]
                
                text = self.chess_board_square_to_string(space)
                
                square.clean_square()
                square.write_to_square(text)
        
    def is_active_players_piece(self,pos):
        active_player = self.maingui.chessmain.board.active_player
        row, column = pos
        active_piece = self.maingui.chessmain.board.mat[row][column]
        if isinstance(active_piece,str):
            return False
        return active_player == active_piece.color
    
    def valid_moves_for_selected_piece(self):
        row, column = self.selected_square
        piece = self.maingui.chessmain.board.mat[row][column]
        valid_moves = piece.validMoves()
        return valid_moves
    
    def try_select(self,pos):
        if self.is_active_players_piece(pos):
            self.selected_square = pos
        return self.is_active_players_piece(pos)
        
    #helper functions
    def chess_piece_to_emoji(self,piece):
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
                return "     ♟️"
            # as for the black pawn, i really don't know why this works
            # i especially don't know why this is necessary
            # it seems to be the only way to make this work
            # if you remove the whitespace, the pawn is way off to the left
            # and you can't see it
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
        return None
    # black pawn ♟️
            
    def chess_board_square_to_string(self,list_element):
        if isinstance(list_element,str):
            return ''
        else:
            return self.chess_piece_to_emoji(list_element)

    def stop_game(self,winning_player):
        self.game_over = True
        self.create_game_over_graphic(winning_player)
        
    def start_game(self):
        self.destroy_temp_graphics()
        self.game_over = False

    def destroy_temp_graphics(self):
        try:
            self.temp_graphic.destroy()
            self.temp_graphic2.destroy()
        except:
            pass

    def create_game_over_graphic(self,winning_player):
        # Load the image
        horsey = Image.open('horsey.png')
    
        # Resize the image to fit the square size
        square_size = min(self.winfo_width(), self.winfo_height())
        horsey = horsey.resize((square_size, square_size), Image.NEAREST)
    

        # Convert the image to a PhotoImage object
        tk_image = ImageTk.PhotoImage(horsey)
    
        # Create a label with the image
        label = tk.Label(self, image=tk_image)
        label.image = tk_image  # Keep a reference to the image to prevent garbage collection
    
        label2 = tk.Label(self, text=winning_player+' Wins', font=('Arial',40))
        
        # Place the label on the center square
        label2.place(relx=0.5,rely=0.9,anchor=tk.CENTER,relwidth=1.0,relheight=0.1)
        label.place(relx=0.5,rely=0.4,anchor=tk.CENTER,relwidth=0.8,relheight=0.8)
        self.temp_graphic = label
        self.temp_graphic2 = label2
        self.render_pieces()
        
class BoardSquare(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.text = ''
        self.textID = 1
    
    # add blue dot to self
    def blue_dot_myself(self):
        canvas_width = self.winfo_reqwidth()
        canvas_height = self.winfo_reqheight()
        middle_x = canvas_width // 2
        middle_y = canvas_height // 2
        dot_radius = canvas_height // 8  # Adjust the radius of the dot as needed

        # Calculate the coordinates for the oval
        x1 = middle_x - dot_radius
        y1 = middle_y - dot_radius
        x2 = middle_x + dot_radius
        y2 = middle_y + dot_radius

        # Create the oval shape (blue dot) at the middle of the canvas
        self.create_oval(x1, y1, x2, y2, fill="blue")
    
    # initialize_square
    def write_to_square(self,text):
        self.textID = self.create_center_text(text)
        self.textID = self.center_text()
        
    # resize_square
    def resize_square(self):
        self.textID = self.center_text()
    
    # clean_square
    def clean_square(self):
        self.delete("all")
    
    # creates a piece of text centered in canvas
    # returns the text ID
    def create_center_text(self, text):
        textID = self.create_text(1, 1, text=text, font=("Arial", 1))
        return textID
    
    # resizes and recenters the contained text
    def center_text(self):
        # Get the dimensions of the canvas
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        
        # Calculate the maximum font size based on canvas dimensions and character size
        max_font_size = min(canvas_width, canvas_height) // (len(self.text) + 1)
        max_font_size = int(max_font_size*0.7)
        
        # Calculate the center coordinates
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        
        self.coords(self.textID, center_x, center_y)
        self.itemconfig(self.textID, font=('Arial',max_font_size))
        return self.textID
        

    
    

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Chess Board")

#     chess_board = ChessBoardGUI(root)
#     chess_board.pack(expand=True, fill="both")
    
#     root.geometry('400x400')
#     root.mainloop()
    