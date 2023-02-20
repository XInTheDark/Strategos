# Strategos chess engine, written in Python.
import chess

import bitboard
from engine_types import *

class Position:
    board: bitboard.Board = None
    
    # en passant square
    en_passant = None
    
    # castling rights
    castling = [True, True, True, True]
    
    # game ply
    game_ply = 0
    
    # side to move
    side_to_move = True  # True = white, False = black
    
    def __init__(self, fen=None):
        self.board = bitboard.Board(fen)
        # obtain information from the FEN string
        chess_board = self.board.chess_board()
        
        self.en_passant = chess_board.ep_square
        self.castling = [chess_board.has_kingside_castling_rights(chess.WHITE),
                            chess_board.has_queenside_castling_rights(chess.WHITE),
                            chess_board.has_kingside_castling_rights(chess.BLACK),
                            chess_board.has_queenside_castling_rights(chess.BLACK)]
        
        self.game_ply = chess_board.fullmove_number
        self.side_to_move = chess_board.turn
        
    def fen(self):
        return self.board.fen()

    def legal_moves(self):
        return self.board.chess_board().legal_moves
    
    def material(self, side_to_move: chess.Color, phase=MIDDLEGAME):
        return self.board.material(side_to_move=side_to_move, phase=phase)
    
    def game_phase(self):
        """currently uses a primitive material count to determine the game phase"""
        m = self.material(chess.WHITE) + self.material(chess.BLACK)
        if m < QUEEN_VALUE_EG * 2:
            return ENDGAME
        else:
            return MIDDLEGAME
        
    def pawn_passed(self) -> bool:
        # check if there is a passed pawn.
        # TODO: implement this
        pass
    
    