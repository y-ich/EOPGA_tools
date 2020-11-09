"""
check if main line and variations of each SGF is legal.
"""
__author__ = "ICHIKAWA, Yuji <ichikawa.yuji@gmail.com>"

import sys
import os
from multiprocessing import Pool
import psutil
import sgf
from board import Board, move2ev, move2str
from utilities import file_pathes_under

def check_node(node: sgf.Node, board: Board):
    b = Board()
    board.copy(b)
    n = node
    while n is not None:
        move = n.properties.get("B", n.properties.get("W", None))
        if move is None:
            continue
        if b.play(move2ev(move[0])) != 0:
            return False
        n = n.next
    return True

def check_game(game: sgf.GameTree):
    board = Board()
    number = 0
    for node in game.rest:
        v = node.next_variation
        while v is not None:
            if not check_node(v, board):
                return False
            v = v.next_variation
        move = node.properties.get("B", node.properties.get("W", None))
        if move is None:
            continue
        if board.play(move2ev(move[0])) != 0:
            return False
        number += 1
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
