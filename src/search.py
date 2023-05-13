# Strategos chess engine, written in Python.
# search.py contains the search function for the engine.

import evaluate
import position
import uci
from engine_types import *
import stop_search
import eval_psqt

nodes = 0
    
def search(pos: position.Position, depth: int, alpha: int, beta: int, side_to_move: chess.Color, root: bool = False):
    global nodes
    best_move = None
    """Search the position to a given depth."""
    
    if depth == 0:
        nodes += 1
        return evaluate.evaluate(pos, side_to_move), best_move
    
    if pos.board.chess_board().is_game_over():
        return None, None
    
    value = -VALUE_INF
    
    for move in list(pos.board.chess_board().legal_moves):
        if stop_search.search_has_stopped():
            return value, best_move
        
        pos.board.chess_board().push(move)

        # search for checkmate and stalemate
        if pos.board.chess_board().is_checkmate():
            value = max(value, VALUE_MATE + depth)
        elif pos.board.chess_board().is_stalemate():
            value = max(value, VALUE_DRAW)
        
        score = -search(pos, depth - 1, -beta, -alpha, not side_to_move)[0]
        pos.board.chess_board().pop()
        
        if score is not None and score > value:
            value = score
            best_move = move
            
        alpha = max(alpha, value)
        if alpha >= beta:
            break
            
    return value, best_move
    
def iterative_deepening(pos: position.Position, max_depth: int, side_to_move: chess.Color, move_time: int=None):
    import time
    starttime = time.time()
    if move_time is not None:
        stop_search.set_time_limit(move_time / 1000)
    
    global best_move
    for depth in range(1, max_depth + 1):
        score, best_move = search(pos, depth, -VALUE_INF, VALUE_INF, side_to_move, root=True)
        if best_move is not None:
            best_move = uci.move_to_uci(best_move)
        
        t = int((time.time() - starttime) * 1000)
        score = round(score)
        s = f"info depth {depth} seldepth {depth} multipv 1 score cp {score} nodes {nodes} nps {1000 * nodes // t if t else 0} hashfull 0 tbhits 0 time {t} pv {best_move}"
        
        # special case: mate in x
        if score > VALUE_MATE:
            s = s.replace(f"cp {score}", f"mate {score - VALUE_MATE}")
        elif score < -VALUE_MATE:
            s = s.replace(f"cp {score}", f"mate -{abs(score) - VALUE_MATE}")
        
        print(s)  # TODO: Add proper pv output
        
        if stop_search.search_has_stopped():
            # search has stopped, output final bestmove
            print(f"bestmove {best_move} ponder 0000")  # we print ponder as well, even though we don't support it
            break
            
    print(f"bestmove {best_move} ponder 0000")