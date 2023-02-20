# Strategos chess engine, written in Python.

import position
from engine_types import *

def pawn_passed(pos: position.Position, pawn: chess.Square, side_to_move: chess.Color):
    """Return true if the pawn is passed."""
    FILE = chess.square_file(pawn)
    RANK = chess.square_rank(pawn)
    
    # if the pawn is on the 7th rank, it is passed without needing to check
    if RANK == 7-1:
        return True
    
    # if there are no enemy pawns on the same file, or on the two adjacent files, the pawn is passed
    for pawn in pos.board.chess_board().pieces(chess.PAWN, not side_to_move):
        if chess.square_file(pawn) == FILE or chess.square_file(pawn) == FILE-1 or chess.square_file(pawn) == FILE+1:
            def greater_than_rank(r):
                if side_to_move == chess.WHITE:
                    return r > RANK
                else:
                    return r < RANK
            if not greater_than_rank(chess.square_rank(pawn)):
                return False
            
    return True
