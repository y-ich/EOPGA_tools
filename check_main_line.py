"""
check if main line of each SGF is legal.
"""
__author__ = "ICHIKAWA, Yuji <ichikawa.yuji@gmail.com>"

import sys
import os
from multiprocessing import Pool
import psutil
import sgf
from board import Board, move2ev
from utilities import file_pathes_under

def check_game(game: sgf.GameTree):
    board = Board()
    for node in game.rest:
        move = node.properties.get("B", node.properties.get("W", None))
        if move is None:
            continue
        if board.play(move2ev(move[0])) != 0:
            return False
    return True

def check(sgf_path: str):
    with open(sgf_path) as f:
        collection = sgf.parse(f.read())
    for game in collection:
        if not check_game(game):
            return False
    return True

def check_and_arg(e: any):
    """
    is defined explicitly because Pool instance cannot treat lambda function lambda e: (check(e), e).
    """
    return check(e), e

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} <directory>".format(sys.argv[0]))
        sys.exit(0)
    with Pool(psutil.cpu_count(logical=False)) as pool:
        for result, filename in pool.imap_unordered(check_and_arg, file_pathes_under(sys.argv[1], "sgf"), 10):
            if not result:
                print(filename)
