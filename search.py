# Strategos chess engine, written in Python.
import chess
# search.py contains the search function for the engine.

import evaluate
import position
import uci
from engine_types import *
import stop_search
import eval_psqt

nodes = 0

killers = []

best_score = -VALUE_INF
best_move = None
max_score = -VALUE_INF; min_score = VALUE_INF

def prune(pos: position.Position, move: chess.Move, alpha: int, beta: int, side_to_move: chess.Color, depth: int):
    """Prune the search tree."""
    global killers
    
    if abs(evaluate.evaluate(pos, side_to_move)) > 750:
        return False
    
    # if pos.board.chess_board().is_capture(move):
    #     if evaluate.see_eval(pos, side_to_move, move) < -50:
    #         return True
    
    if eval_psqt.eval_psqt_single(move.to_square, pos.board.chess_board().piece_at(move.from_square).piece_type, side_to_move, pos.game_phase()) < -50:
        killers.append(move)
        return True
    
    pos.board.chess_board().push(move)
    e = evaluate.evaluate(pos, side_to_move)
    pos.board.chess_board().pop()
    if e < alpha - 200 and abs(e) < 500:
        return True
    
    
def search(pos: position.Position, depth: int, alpha: int, beta: int, side_to_move: chess.Color, root: bool = False):
    global nodes, best_score, best_move, max_score, min_score
    bestMove = None
    """Search the position to a given depth."""
    
    if depth == 0 or pos.board.chess_board().is_game_over():
        nodes += 1
        return evaluate.evaluate(pos, side_to_move), None

    if side_to_move == chess.WHITE:
        max_score = -VALUE_INF
        for move in list(pos.board.chess_board().legal_moves):
            if bestMove is None: bestMove = move
            # do we need to stop searching?
            # (either a `stop` command was received, or we've reached the allocated time)
            if stop_search.search_has_stopped():
                return best_score, best_move
            
            # search for checkmate and stalemate first
            if pos.board.chess_board().is_checkmate():
                max_score = best_score = VALUE_MATE + depth
                best_move = move
                return VALUE_MATE + depth, move
            elif pos.board.chess_board().is_stalemate() and max_score < VALUE_DRAW:
                max_score = best_score = VALUE_DRAW
                best_move = move
                return VALUE_DRAW, move
            
            # TODO: implement proper pruning
            if prune(pos, move, alpha, beta, side_to_move, depth):
                continue
            
            pos.board.chess_board().push(move)
            nodes += 1
            score, _ = search(pos, depth - 1, alpha, beta, chess.BLACK)
            score = -score
            pos.board.chess_board().pop()
        
            if score > max_score:
                max_score = score
                if max_score > best_score:
                    bestMove = move
                
            if root and score > best_score:
                best_move = bestMove
        
            beta = (alpha + beta) // 2
            alpha = max(alpha, max_score)
            
            if beta <= alpha:
                break
    
        return max_score, bestMove
    
    else: # side_to_move == chess.BLACK
        min_score = float('inf')
        for move in list(pos.board.chess_board().legal_moves):
            if bestMove is None: bestMove = move
            # do we need to stop searching?
            # (either a `stop` command was received, or we've reached the allocated time)
            if stop_search.search_has_stopped():
                return min_score, best_move
            
            # search for checkmate and stalemate
            if pos.board.chess_board().is_checkmate():
                min_score = best_score = -(VALUE_MATE + depth)
                best_move = move
                return -(VALUE_MATE + depth), move
            elif pos.board.chess_board().is_stalemate() and min_score > VALUE_DRAW:
                min_score = best_score = VALUE_DRAW
                best_move = move
                return VALUE_DRAW, move
            
            if prune(pos, move, alpha, beta, side_to_move, depth):
                continue
                
            pos.board.chess_board().push(move)
            nodes += 1
            score, _ = search(pos, depth - 1, alpha, beta, chess.WHITE)
            score = -score
            pos.board.chess_board().pop()
        
            if score < min_score:
                min_score = score
                if min_score < best_score or best_score == -VALUE_INF:
                    bestMove = move
                
            if root and min_score < best_score:
                best_move = bestMove
        
            beta = (alpha + beta) // 2
            alpha = min(alpha, min_score)
            
            if beta <= alpha:
                break
    
        return min_score, bestMove
    
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
            
        # sometimes we increase a depth if the score is extremely high
        if depth < 6 and abs(evaluate.evaluate(pos, side_to_move)) > 500:
            depth += 1
            
    print(f"bestmove {best_move} ponder 0000")