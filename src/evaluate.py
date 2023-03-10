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
            try:
                capturingPieceV = material_(board.piece_at(move.from_square).piece_type, pos.game_phase())
                capturedPieceV = material_(board.piece_at(move.to_square).piece_type, pos.game_phase())
            except AttributeError:
                continue
            if capturedPieceV > capturingPieceV or board.attackers(not side_to_move, move.to_square).__len__() == 0:
                hangingEval += capturedPieceV - capturingPieceV
                
                # additionally, if the capturingPiece is a pawn, we add a large bonus
                if board.piece_at(move.from_square).piece_type == chess.PAWN:
                    hangingEval += 100
                    
                # also, if the capturingPiece is not attacked after the capture,
                # we do not subtract its value from the hangingEval
                if not board.is_attacked_by(not side_to_move, move.to_square):
                    hangingEval += capturingPieceV
    
    v = materialEval + psqtEval + hangingEval
    
    # Step 3.5 Check if WE are hanging material too.
    hangingEval = 0
    # First do a null move.
    board.push(chess.Move.null())
    for move in list(board.legal_moves):
        if board.is_capture(move):
            try:
                capturingPieceV = material_(board.piece_at(move.from_square).piece_type, pos.game_phase())
                capturedPieceV = material_(board.piece_at(move.to_square).piece_type, pos.game_phase())
            except AttributeError:
                continue
                
            if capturedPieceV > capturingPieceV or board.attackers(side_to_move, move.to_square).__len__() == 0:
                hangingEval -= capturedPieceV - capturingPieceV
                
                # additionally, if the capturingPiece is a pawn, we add a large bonus
                if board.piece_at(move.from_square).piece_type == chess.PAWN:
                    hangingEval -= 100
                    
                # also, if the capturingPiece is not attacked after the capture,
                # we do not subtract its value from the hangingEval
                if not board.is_attacked_by(side_to_move, move.to_square):
                    hangingEval -= capturingPieceV
                    
    board.pop()  # unmake the null move
    v -= hangingEval
    
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
    
    # Step 5. Penalty for doubled and isolated pawns.
    # Check only in endgame.
        for side in [side_to_move, not side_to_move]:
            for pawn in pos.doubled_pawns(side):
                v += (15 if pos.game_phase() == MIDDLEGAME else 35) * (1 if side != side_to_move else -1)
        
        for side in [side_to_move, not side_to_move]:
            for pawn in pos.isolated_pawns(side):
                v += (15 if pos.game_phase() == MIDDLEGAME else 60) * (1 if side != side_to_move else -1)
    
    # Step 6. Penalty for pinned pieces, and bonus for pinning pieces.
    # Check only in middlegame.
    if pos.game_phase() == MIDDLEGAME:
        for pieceType in PIECE_TYPES:
            for piece in board.pieces(pieceType, side_to_move):
                if board.is_pinned(side_to_move, piece):
                   v -= material_(pieceType, pos.game_phase()) / 3
                   if board.attackers(not side_to_move, piece).__len__() >= 1:
                       v -= material_(pieceType, pos.game_phase()) / 2
            for piece in board.pieces(pieceType, not side_to_move):
                if board.is_pinned(not side_to_move, piece):
                    v += material_(pieceType, pos.game_phase()) / 3
                    if board.attackers(side_to_move, piece).__len__() >= 1:
                        v += material_(pieceType, pos.game_phase()) / 2
    
        # Step 7. Bonus for attacking a piece multiple times
        for color in [side_to_move, not side_to_move]:
            for pieceType in PIECE_TYPES:
                for piece in board.pieces(pieceType, not color):
                    if board.attackers(color, piece).__len__() >= 2:
                        v += material_(pieceType, pos.game_phase()) / 4 * (1 if color == side_to_move else -1)
                    
    return v


def see_eval(pos: position.Position, side_to_move: chess.Color, capture: chess.Move):
    # TODO: Fix error at "pos.board.chess_board().pop()"
    """Return the static exchange evaluation of a capture."""
    
    capturingPiece = pos.board.chess_board().piece_at(capture.from_square)
    capturedPiece = pos.board.chess_board().piece_at(capture.to_square)
    
    if capturedPiece is None:
        return 0  # this should only happen for en passant captures, which is PAWN takes PAWN = 0.
    
    capturingV = material_(capturingPiece.piece_type, pos.game_phase())
    capturedV = material_(capturedPiece.piece_type, pos.game_phase())
    
    if capturingV > capturedV and pos.board.chess_board().attackers(
            not side_to_move, capture.to_square).__len__() >= 1:
        return capturedV - capturingV  # negative
    
    # make the capture
    pos.board.chess_board().push(capture)
    e = evaluate(pos, side_to_move)
    pos.board.chess_board().pop()
    
    if e > 0:
        return capturedV - capturingV
    else:
        return capturedV - capturingV + e  # penalty for negative eval after capture