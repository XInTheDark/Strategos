# Strategos chess engine, written in Python.

# evaluate.py contains the evaluation function for the engine.

import position
from engine_types import *
import eval_psqt
import pieces
import endgame

def evaluate(pos: position.Position, side_to_move: chess.Color):
    """Evaluate the position from side to move's POV."""
    
    # Step 0. If <= 7 pieces, use an endgame tablebase in endgame.py.
    if config.USE_ONLINE_TABLEBASE and pos.count_all_pieces() <= 7:
        return endgame.query_tablebase(pos, side_to_move)
    
    # Step 1. Material evaluation.
    board = pos.board.chess_board()
    US_MATERIAL = pos.material(side_to_move)
    THEM_MATERIAL = pos.material(not side_to_move)
        
    materialEval = US_MATERIAL - THEM_MATERIAL
    
    # Step 2. Piece-square bonuses.
    psqtEval = eval_psqt.eval_psqt(pos, side_to_move, pos.game_phase()) \
               - eval_psqt.eval_psqt(pos, not side_to_move, pos.game_phase())
    
    # Step 3. Treat hanging pieces as if they were material.
    hangingEval = 0
    for move in list(board.legal_moves):
        if board.is_capture(move):
            capturingPieceV = material_(board.piece_at(move.from_square).piece_type, pos.game_phase())
            capturedPieceV = material_(board.piece_at(move.to_square).piece_type, pos.game_phase())
            if capturedPieceV > capturingPieceV:
                hangingEval += capturedPieceV - capturingPieceV
                
                # additionally, if the capturingPiece is a pawn, we add a large bonus
                if board.piece_at(move.from_square).piece_type == chess.PAWN:
                    hangingEval += 100
                    
                # also, if the capturingPiece is not attacked after the capture,
                # we do not subtract its value from the hangingEval
                if not board.is_attacked_by(not side_to_move, move.to_square):
                    hangingEval -= capturedPieceV
    
    v = materialEval + psqtEval + hangingEval
    
    # Step 4. Bonus for passed pawns.
    if pos.game_phase() == ENDGAME:
        for pawn in board.pieces(chess.PAWN, side_to_move):
            if pieces.pawn_passed(pos, pawn, side_to_move):
                # The more advanced the pawn is, the more valuable it is.
                v += 100 * chess.square_rank(pawn) if side_to_move == chess.WHITE\
                    else 100 * (7 - chess.square_rank(pawn))
                
        # similarly do the same for the enemy pawns, but subtract the value
        for pawn in board.pieces(chess.PAWN, not side_to_move):
            if pieces.pawn_passed(pos, pawn, not side_to_move):
                v -= 100 * (7 - chess.square_rank(pawn)) if side_to_move == chess.WHITE\
                    else 100 * chess.square_rank(pawn)
    
    return v