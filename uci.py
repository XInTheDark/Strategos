# Strategos chess engine, written in Python.

# uci.py contains the UCI interface for the engine.

import chess
import position
import search
from engine_types import *

def move_to_uci(move: chess.Move):
    """Convert a chess.Move object to a UCI string."""
    return move.uci()

def uci_to_move(uci: str):
    """Convert a UCI string to a chess.Move object."""
    return chess.Move.from_uci(uci)

def uci():
    """Start the UCI interface."""
    pos = position.Position()
    while True:
        command = input()
        if command == "uci":
            print("id name Strategos")
            print("id author Muzhen J")
            print("uciok")
        elif command == "isready":
            print("readyok")
        elif command == "ucinewgame":
            pos = position.Position()
        elif command == "position startpos":
            pos = position.Position()
        elif command.startswith("position startpos moves"):
            moves = command.split(" ")[3:]
            for move in moves:
                pos.board.chess_board().push(uci_to_move(move))
        elif command.startswith("position fen moves"):
            fen = command.split(" ")[2]
            moves = command.split(" ")[4:]
            pos = position.Position(fen)
            for move in moves:
                pos.board.chess_board().push(uci_to_move(move))
        elif command.startswith("position fen"):
            fen = command.split(" ")[2]
            pos = position.Position(fen)
        elif command.startswith("go"):
            if command.split(" ").__len__() > 1 and command.split(" ")[1].split("=")[0] == "depth":
                depth = int(command.split(" ")[1].split("=")[1])
            else:
                depth = MAX_DEPTH
            search.iterative_deepening(pos, depth, pos.board.chess_board().turn)
        elif command == "quit" or command == "stop":
            break
