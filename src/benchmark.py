# Strategos chess engine, written in Python.

# benchmark.py contains the benchmarking code for the engine.
# It is called when the "bench" command is given.

import time

import position
import search
from engine_types import *

fens = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 10",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 11",
    "4rrk1/pp1n3p/3q2pQ/2p1pb2/2PP4/2P3N1/P2B2PP/4RRK1 b - - 7 19",
    "rq3rk1/ppp2ppp/1bnpN3/3N2B1/4P3/7P/PPPQ1PP1/2KR3R b - - 0 14",
    "r1bq1r1k/1pp1n1pp/1p1p4/4p2Q/4PpP1/1BNP4/PPP2P1P/3R1RK1 b - g3 0 14",
    "r3r1k1/2p2ppp/p1p1bn2/8/1q2P3/2NPQN2/PPP3PP/R4RK1 b - - 2 15",
    "r1bbk1nr/pp3p1p/2n5/1N4p1/2Np1B2/8/PPP2PPP/2KR1B1R w kq - 0 13",
    "r1bq1rk1/ppp1nppp/4n3/3p3Q/3P4/1BP1B3/PP1N2PP/R4RK1 w - - 1 16",
    "4r1k1/r1q2ppp/ppp2n2/4P3/5Rb1/1N1BQ3/PPP3PP/R5K1 w - - 1 17",
]

def benchmark_fen(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth=5):
    """Run a benchmark to get # of nodes searched up to a certain depth."""
    pos = position.Position(fen)
    startNodes = search.nodes
    start = time.time()
    search.iterative_deepening(pos, depth, pos.side_to_move)
    end = time.time()
    n = search.nodes - startNodes
    
    return n, round(end - start, 2)  # nodes, time
    
def benchmark():
    """Run a benchmark for a set of FENs."""
    egtb_enable = config.USE_ONLINE_TABLEBASE
    if egtb_enable:
        config.USE_ONLINE_TABLEBASE = False
    
    nodes = totalTime = 0
    for fen in fens:
        print(f"\nposition fen {fen}")
        n, t = benchmark_fen(fen)
        nodes += n
        totalTime += t
    
    print(f"Nodes searched: {nodes}")
    print(f"Time taken: {round(totalTime, 2)}s")
    print(f"Nodes per second: {round(nodes / totalTime, 2)}")
    
    # reset the egtb setting
    config.USE_ONLINE_TABLEBASE = egtb_enable