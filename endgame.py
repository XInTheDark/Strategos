# Strategos chess engine, written in Python.

# endgame.py contains the endgame evaluation function.
# It uses an online tablebase to evaluate positions with <= 7 pieces.
# We currently use the lila tablebase hosted by lichess.org.

import position
from engine_types import *

def query_tablebase(pos: position.Position, side_to_move: chess.Color):
    """Query the online tablebase for the position."""
    """https://github.com/lichess-org/lila-tablebase"""
    
    # We assume that config.USE_ONLINE_TABLEBASE is True when this function is called.
    import requests
    
    FEN = pos.fen()
    LINK = "http://tablebase.lichess.ovh/standard?fen=" + FEN
    r = requests.get(LINK)  # if this fails, then the user should disable USE_ONLINE_TABLEBASE
    j = r.json()
    
    eval_ = j["category"] # "win", "loss", "draw"
    
    if eval_ == "win":
        return VALUE_MATE + j["dtm"]
    elif eval_ == "loss":
        return -(VALUE_MATE + j["dtm"])
    else:
        return VALUE_DRAW

    