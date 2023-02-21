# Strategos chess engine, written in Python.

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
        
        self.game_ply = chess_board.ply()
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
        # implemented in pieces.py!
        pass
    
    def all_pieces(self):
        """Returns a list of all pieces on the board."""
        pieces = []
        
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in PIECE_TYPES:
                for piece in self.board.chess_board().pieces(piece_type=piece_type, color=color):
                    pieces.append(piece)
        
        return pieces
    
    def count_all_pieces(self):
        """Returns the number of pieces on the board."""
        return len(self.all_pieces())
    
    def move_is_stm(self, move: chess.Move):
        # assumes that the move is in pos.board.chess_board().legal_moves
        # checks if the moved piece has same color as side to move
        return self.board.chess_board().piece_at(move.from_square).color == self.side_to_move
    