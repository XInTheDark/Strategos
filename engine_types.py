# Strategos chess engine, written in Python.

# engine_types.py contains the types that will be used throughout the engine.

import chess

# 1. Material values in centipawns.
PAWN_VALUE_MG = 99; KNIGHT_VALUE_MG = 300; BISHOP_VALUE_MG = 320; ROOK_VALUE_MG = 500; QUEEN_VALUE_MG = 900; KING_VALUE_MG = 50000
PAWN_VALUE_EG = 149; KNIGHT_VALUE_EG = 279; BISHOP_VALUE_EG = 349; ROOK_VALUE_EG = 600; QUEEN_VALUE_EG = 1100; KING_VALUE_EG = 50000

# 2. Game phase
MIDDLEGAME = 0; ENDGAME = 1

# 3. Piece types
PIECE_TYPES = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

# 4. Evaluation values
VALUE_INF = 1000000; VALUE_MATE = 10000001; VALUE_MATED = -10000001; VALUE_DRAW = 0; VALUE_NONE = None

# 5. Depth
MAX_DEPTH = 64

def material_(piece, phase=MIDDLEGAME):
    """Return the material value of a piece, in middlegame/endgame values depending on the phase."""
    if phase == MIDDLEGAME:
        if piece == chess.PAWN:
            return PAWN_VALUE_MG
        elif piece == chess.KNIGHT:
            return KNIGHT_VALUE_MG
        elif piece == chess.BISHOP:
            return BISHOP_VALUE_MG
        elif piece == chess.ROOK:
            return ROOK_VALUE_MG
        elif piece == chess.QUEEN:
            return QUEEN_VALUE_MG
        elif piece == chess.KING:
            return KING_VALUE_MG
    elif phase == ENDGAME:
        if piece == chess.PAWN:
            return PAWN_VALUE_EG
        elif piece == chess.KNIGHT:
            return KNIGHT_VALUE_EG
        elif piece == chess.BISHOP:
            return BISHOP_VALUE_EG
        elif piece == chess.ROOK:
            return ROOK_VALUE_EG
        elif piece == chess.QUEEN:
            return QUEEN_VALUE_EG
        elif piece == chess.KING:
            return KING_VALUE_EG
    return None
