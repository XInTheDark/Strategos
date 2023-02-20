# Strategos chess engine, written in Python.
import threading

STOP_SEARCH = False

def stop_search():
    global STOP_SEARCH
    STOP_SEARCH = True
    
def search_has_stopped():
    return STOP_SEARCH

def set_time_limit(time_limit: float):
    """sets a time limit for the search to stop after (in seconds)"""
    threading.Timer(time_limit, stop_search).start()