# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:58:07 2024

@author: neeb-meister

Utils
"""
# the goal of this class is to provide a package of utilities needed by the pieces
# and by the board module

import json
import os

class ChessUtils:
    def __init__(self):
        self.name = "ChessUtils"
    # open_txt_file :
    # creates a console prompt to select a txt file in the current directory
    def open_txt_file(cls):
        # Get a list of all the .txt files in the current directory
        txt_files = [file for file in os.listdir() if file.endswith('.txt')]
        
        if not txt_files:
            print("No .txt files found in the current directory.")
            return
        
        # Print the list of .txt files
        print("Select a .txt file to open:")
        for i, file in enumerate(txt_files, start=1):
            print(f"{i}. {file}")
        
        # Prompt the user to select a file
        while True:
            try:
                choice = int(input("Enter the number of the file you want to open: "))
                if 1 <= choice <= len(txt_files):
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Open the selected file
        selected_file = txt_files[choice - 1]
        with open(selected_file, 'r') as file:
            data = json.load(file)
            return data
    
    # not2int : string -> [int,int]
    # takes a notation string "a8" and translates it to int index [0,0]
    def not2int(cls,notation,col=None):
        #return in format provided
        if col == None and type(notation)==list:
            row = notation[1]
            column = notation[0]
            row = 8 - row
            column = ord(column)-97
            return [row,column]
        elif col ==None:
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
    def int2not(cls,integer,col=None):
        #return in format provided
        if col == None:
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
    def notq(cls,string):
        try:
            ints = cls.not2int(string)
            if ints[0] in range(8) and ints[1] in range(8):
                return True
            return False
        except:
            return False