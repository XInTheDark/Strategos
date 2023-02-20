# Strategos chess engine, written in Python.
import chess

# eval_psqt.py contains the piece-square tables for knight, bishop, rook, queen, pawn and king.

import position
from engine_types import *

# piece-square tables
# table[i][j] is the bonus for the piece when it is on square[i][j].
# It is a tuple of (middlegame, endgame) values.

# Pawn
# In C++ it is written as:
# { S(  2, -8), S(  4, -6), S( 11,  9), S( 18,  5), S( 16, 16), S( 21,  6), S(  9, -6), S( -3,-18) },
#    { S( -9, -9), S(-15, -7), S( 11,-10), S( 15,  5), S( 31,  2), S( 23,  3), S(  6, -8), S(-20, -5) },
#    { S( -3,  7), S(-20,  1), S(  8, -8), S( 19, -2), S( 39,-14), S( 17,-13), S(  2,-11), S( -5, -6) },
#    { S( 11, 12), S( -4,  6), S(-11,  2), S(  2, -6), S( 11, -5), S(  0, -4), S(-12, 14), S(  5,  9) },
#    { S(  3, 27), S(-11, 18), S( -6, 19), S( 22, 29), S( -8, 30), S( -5,  9), S(-14,  8), S(-11, 14) },
#    { S( -7, -1), S(  6,-14), S( -2, 13), S(-11, 22), S(  4, 24), S(-14, 17), S( 10,  7), S( -9,  7) }

PAWN_PSQT = [
    [(0, 0)] * 8,
    [ (2, -8), (4, -6), (11, 9), (18, 5), (16, 16), (21, 6), (9, -6), (-3, -18) ],
    [ (-9, -9), (-15, -7), (11, -10), (15, 5), (31, 2), (23, 3), (6, -8), (-20, -5) ],
    [ (-3, 7), (-20, 1), (8, -8), (19, -2), (39, -14), (17, -13), (2, -11), (-5, -6) ],
    [ (11, 12), (-4, 6), (-11, 2), (2, -6), (11, -5), (0, -4), (-12, 14), (5, 9) ],
    [ (3, 27), (11, 18), (6, 19), (22, 29), (8, 30), (5, 9), (14, 8), (11, 14) ],
    [ (25, 50), (30, 51), (31, 52), (50, 75), (50, 75), (31, 52), (30, 51), (25, 50) ],
    [(0, 0)] * 8
]

# Knight
KNIGHT_PSQT = [
    [ (-50, -50), (-40, -40), (-30, -30), (-30, -30), (-30, -30), (-30, -30), (-40, -40), (-50, -50) ],
    [ (-40, -40), (-20, -20), (0, 0), (0, 0), (0, 0), (0, 0), (-20, -20), (-40, -40) ],
    [ (-30, -30), (0, 0), (10, 10), (15, 15), (15, 15), (10, 10), (0, 0), (-30, -30) ],
    [ (-30, -30), (5, 5), (15, 15), (20, 20), (20, 20), (15, 15), (5, 5), (-30, -30) ],
    [ (-30, -30), (0, 0), (15, 15), (20, 20), (20, 20), (15, 15), (0, 0), (-30, -30) ],
    [ (-30, -30), (5, 5), (10, 10), (15, 15), (15, 15), (10, 10), (5, 5), (-30, -30) ],
    [ (-40, -40), (-20, -20), (0, 0), (5, 5), (5, 5), (0, 0), (-20, -20), (-40, -40) ],
    [ (-50, -50), (-40, -40), (-30, -30), (-30, -30), (-30, -30), (-30, -30), (-40, -40), (-50, -50) ]
]

# Bishop
# TODO: add bishop psqt
BISHOP_PSQT = [[(0, 0)] * 8] * 8

# Rook
ROOK_PSQT = [
    [ (0, 0), (0, 0), (0, 0), (10, 0), (10, 0), (0, 0), (0, 0), (0, 0) ],
    [(0, 0)] * 8,
    [(0, 0)] * 8,
    [(0, 0)] * 8,
    [(0, 0)] * 8,
    [(0, 0)] * 8,
    # rooks on the 7th rank are more valuable
    [ (20, 15), (35, 15), (30, 15), (23, 15), (23, 15), (30, 15), (35, 15), (20, 15) ],
    [(0, 0)] * 8
]

# Queen
# TODO: add queen psqt
QUEEN_PSQT = [[(0, 0)] * 8] * 8

# King
KING_PSQT = [
    [ (30, -60), (50, -50), (-20, -40), (-10, -10), (-10, -10), (-20, -40), (30, -50), (50, -60) ],
    [ (20, -50), (-30, -40), (-20, -30), (-10, 0), (-10, 0), (-20, -30), (-30, -40), (20, -50) ],
    [ (-10, -10), (-20, 30), (-20, 20), (-30, 10), (-30, 10), (-20, 20), (-20, 30), (10, -10) ],
    [ (-20, 10), (-20, 40), (-20, 40), (-20, 60), (-20, 60), (-20, 40), (-20, 40), (-20, 10) ],
    [ (-50, 10), (-50, 40), (-60, 45), (-100, 70), (-100, 70), (-60, 45), (-50, 40), (-50, 10) ],
    [ (-100, 10), (-100, 40), (-150, 40), (-200, 70), (-200, 70), (-150, 40), (-100, 40), (-100, 10) ],
    [ (-200, 10), (-250, 40), (-250, 40), (-250, 60), (-250, 60), (-200, 40), (-200, 40), (-200, 10) ],
    [ (-300, -10), (-300, 30), (-350, 50), (-400, 50), (-400, 50), (-300, 50), (-200, 30), (-100, -10) ]
]

def psqt(pieceType: chess.PieceType):
    if pieceType == chess.PAWN:
        return PAWN_PSQT
    elif pieceType == chess.KNIGHT:
        return KNIGHT_PSQT
    elif pieceType == chess.BISHOP:
        return BISHOP_PSQT
    elif pieceType == chess.ROOK:
        return ROOK_PSQT
    elif pieceType == chess.QUEEN:
        return QUEEN_PSQT
    elif pieceType == chess.KING:
        return KING_PSQT
    return None

def eval_psqt_single(square: chess.Square, pieceType: chess.PieceType, side: chess.Color, phase=MIDDLEGAME):
    return psqt(pieceType)[7 - chess.square_rank(square)][chess.square_file(square)][phase]
def eval_psqt_piece(pos: position.Position, side: chess.Color, pieceType: chess.PieceType, phase):
    score = 0
    chess_board = pos.board.chess_board()
    for square in chess.SQUARES:
        piece = chess_board.piece_at(square)
        # if the side is black, flip the psqt
        if piece and piece.piece_type == pieceType and piece.color == side:
            if side == chess.BLACK:
                score += psqt(pieceType)[7 - chess.square_rank(square)][chess.square_file(square)][phase]
            else:
                score += psqt(pieceType)[chess.square_rank(square)][chess.square_file(square)][phase]
    return score

def eval_psqt(pos: position.Position, side: chess.Color, phase):
    score = 0
    for pieceType in chess.PIECE_TYPES:
        score += eval_psqt_piece(pos, side, pieceType, phase)
    return score