# Strategos chess engine, written in Python.

# bitboard.py contains the Board class, which is the representation of the chess board.

class Board:
    SQUARE_EMPTY = 0b000000
    PAWN_W = 0b000001;
    KNIGHT_W = 0b000010;
    BISHOP_W = 0b000011;
    ROOK_W = 0b000100;
    QUEEN_W = 0b000101;
    KING_W = 0b000110
    PAWN_B = 0b000111;
    KNIGHT_B = 0b001000;
    BISHOP_B = 0b001001;
    ROOK_B = 0b001010;
    QUEEN_B = 0b001011;
    KING_B = 0b001100
    
    # We use a 2D array of bits to represent the board.
    # The first 6 bits represent the piece type, and the last 2 bits represent the color.
    
    board = [[0 for x in range(8)] for y in range(8)]
    startpos = [
        [ROOK_W, KNIGHT_W, BISHOP_W, QUEEN_W, KING_W, BISHOP_W, KNIGHT_W, ROOK_W],
        [PAWN_W] * 8,
        [SQUARE_EMPTY] * 8, [SQUARE_EMPTY] * 8, [SQUARE_EMPTY] * 8, [SQUARE_EMPTY] * 8,
        [PAWN_B] * 8,
        [ROOK_B, KNIGHT_B, BISHOP_B, QUEEN_B, KING_B, BISHOP_B, KNIGHT_B, ROOK_B]
    ]
    
    def __init__(self, board=None):
        if board is None:
            # Initialize the board with the starting position.
            board = self.startpos
        # Initialize the board with the given position.
        self.board = board


class Position:
    """The Position class is used in conjunction with the Board class.
    While the Board class only represents the pieces on the board,
    the Position class represents other information about the position,
    such as the en passant square, the castling rights, move count, and side to move."""
    
    board = Board()
    
    # The en passant square is represented by a list of (file, rank).
    # If there is no en passant square, the value is None.
    en_passant = None
    
    # The castling rights are represented by a list of (white_kingside, white_queenside, black_kingside, black_queenside).
    castling = [True, True, True, True]
    
    # The game ply is the number of half-moves made in the game.
    game_ply = 0
    
    # The side to move is represented by a boolean value.
    # True = white, False = black
    side_to_move = True
    
    def __init__(self, board=None, en_passant=None, castling=None, game_ply=0, side_to_move=True):
        if board is None:
            board = Board()
        if castling is None:
            castling = [True, True, True, True]
        self.en_passant = en_passant
        self.castling = castling
        self.game_ply = game_ply
        self.side_to_move = side_to_move
    
    def to_fen(self):
        # example FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        fen = ""


