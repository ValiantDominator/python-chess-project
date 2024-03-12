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

class ChessLog:
    def __init__(self,chessboard):
        self.log = {}
        self.log_stream = ''
        # self.logentry = ''
        self.tn = 0
        
    def write(self,tidbit,flush=False):
        # self.logentry = tidbit
        self.log[self.tn] = tidbit
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
        