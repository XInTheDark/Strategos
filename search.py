# Strategos chess engine, written in Python.
import eval_psqt
# search.py contains the search function for the engine.

import evaluate
import position
import uci
from engine_types import *
import stop_search

nodes = 0

killers = []

best_score = -VALUE_INF
best_move = None

def prune(pos: position.Position, move: chess.Move, alpha: int, beta: int, side_to_move: chess.Color, depth: int):
    """Prune the search tree."""
    global killers
    
    if eval_psqt.eval_psqt_single(move.to_square, pos.board.chess_board().piece_at(move.from_square).piece_type, side_to_move, pos.game_phase()) < 0:
        killers.append(move)
        return True
    
    if depth < 9 and move in killers:
        return True
    
    pos.board.chess_board().push(move)
    e = evaluate.evaluate(pos, side_to_move)
    pos.board.chess_board().pop()
    if e < alpha - 100:
        return True
    
    
def search(pos: position.Position, depth: int, alpha: int, beta: int, side_to_move: chess.Color):
    global nodes, best_score, best_move
    """Search the position to a given depth."""
    # do we need to stop searching?
    # (either a `stop` command was received, or we've reached the allocated time)
    if stop_search.search_has_stopped():
        return best_score, best_move
    
    if depth == 0 or pos.board.chess_board().is_game_over():
        nodes += 1
        return evaluate.evaluate(pos, side_to_move), None

    if side_to_move == chess.WHITE:
        max_score = -VALUE_INF
        for move in list(pos.board.chess_board().legal_moves):
            # do we need to stop searching?
            # (either a `stop` command was received, or we've reached the allocated time)
            if stop_search.search_has_stopped():
                return max_score, best_move
            
            # TODO: implement pruning
            if prune(pos, move, alpha, beta, side_to_move, depth):
                continue
            
            pos.board.chess_board().push(move)
            nodes += 1
            score, _ = search(pos, depth - 1, alpha, beta, chess.BLACK)
            pos.board.chess_board().pop()
        
            if score > max_score:
                max_score = best_score = score
                best_move = move
        
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break
    
        return max_score, best_move
    
    else:
        min_score = float('inf')
        for move in list(pos.board.chess_board().legal_moves):
            # do we need to stop searching?
            # (either a `stop` command was received, or we've reached the allocated time)
            if stop_search.search_has_stopped():
                return min_score, best_move
            
            if prune(pos, move, alpha, beta, side_to_move, depth):
                continue
                
            pos.board.chess_board().push(move)
            nodes += 1
            score, _ = search(pos, depth - 1, alpha, beta, chess.WHITE)
            pos.board.chess_board().pop()
        
            if score < min_score:
                min_score = best_score = score
                best_move = move
        
            beta = min(beta, min_score)
            if beta <= alpha:
                break
    
        return min_score, best_move
    
def iterative_deepening(pos: position.Position, max_depth: int, side_to_move: chess.Color, move_time: int):
    import time
    starttime = time.time()
    if move_time is not None:
        stop_search.set_time_limit(move_time / 1000)
    
    global best_move
    for depth in range(1, max_depth + 1):
        score, best_move = search(pos, depth, -VALUE_INF, VALUE_INF, side_to_move)
        if best_move is not None:
            best_move = uci.move_to_uci(best_move)
        
        t = int((time.time() - starttime) * 1000)
        print(f"info depth {depth} seldepth {depth} multipv 1 score cp {score} nodes {nodes} nps 0 hashfull 0 tbhits 0 time {t} pv {best_move}\n"
              )  # TODO: fix UCI output (including proper nodes count, nps, time and pv)
        
        if stop_search.search_has_stopped():
            # search has stopped, output final bestmove
            print(f"bestmove {best_move} ponder 0000")  # we print ponder as well, even though we don't support it
            break
            
        # sometimes we skip a depth
        if depth < 6 and abs(evaluate.evaluate(pos, side_to_move)) < 100:
            depth += 1
            
    print(f"bestmove {best_move} ponder 0000")