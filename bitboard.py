# Strategos chess engine, written in Python.

# bitboard.py contains the Board class, which is the representation of the chess board.

import chess
from engine_types import *

class Board:
    board = None
    
    def __init__(self, fen=None):
        if fen is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(fen)
    
    def fen(self):
        return self.board.fen()
    
    def chess_board(self):
        """return the chess.Board object, which contains many useful methods"""
        return self.board
    
    def material(self, side_to_move: chess.Color, phase=MIDDLEGAME):
        """Count the pieces on a board, and then return the material value."""
        material = 0
        
        for pieceType in PIECE_TYPES:
            if pieceType == chess.KING: continue
            for piece in self.chess_board().pieces(piece_type=pieceType, color=side_to_move):
                material += material_(pieceType, phase)
        
        return material