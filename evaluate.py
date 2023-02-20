# Strategos chess engine, written in Python.

# evaluate.py contains the evaluation function for the engine.

import position
from engine_types import *
import eval_psqt

def evaluate(pos: position.Position, side_to_move: chess.Color):
    """Evaluate the position from side to move's POV."""
    
    # Step 1. Material evaluation.
    board = pos.board.chess_board()
    US_MATERIAL = pos.material(side_to_move)
    THEM_MATERIAL = pos.material(not side_to_move)
        
    materialEval = US_MATERIAL - THEM_MATERIAL
    
    # Step 2. Piece-square bonuses.
    psqtEval = eval_psqt.eval_psqt(pos, side_to_move, pos.game_phase())
    
    # Step 3. Pawn structure evaluation.
    # TODO
    
    v = materialEval + psqtEval
    
    return v