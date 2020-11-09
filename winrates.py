"""
calculates winrate transition of each SGF.
"""
__author__ = "ICHIKAWA, Yuji <ichikawa.yuji@gmail.com>"

import sys
from multiprocessing import Pool
import psutil
import sgf
from utilities import file_pathes_under

def parse_comment(s: str) -> tuple[float, int]:
    tokens = s.split("\n")
    if len(tokens) != 2:
        raise Exception("invalid string")
    return float(tokens[0]), int(tokens[1])

def winrate_of(node: sgf.Node) -> float:
    """
    The winrate of the node/position is defined as winrate of the most visited child.
    """
    max_visits = 0
    winrate = 0
    variations = ([] if node.next == None else [node.next]) + node.variations
    for child in variations:
        if "B" in child.properties or "W" in child.properties:
            try:
                info = parse_comment(child.properties["C"][0])
                if info[1] > max_visits:
                    max_visits = info[1]
                    winrate = info[0]
            except:
                pass
    if max_visits == 0:
        return None
    return winrate

def winrates_of(game: sgf.GameTree) -> list[float]:
    winrates = []
    node = game.root.next
    assert "B" in node.properties or "W" in node.properties
    winrate, visits = parse_comment(node.properties["C"][0])
    winrates.append(winrate) # I defined winrate of initial position as the winrate of the first move.
    while node is not None:
        if "B" in node.properties or "W" in node.properties:
            winrate = winrate_of(node)
            if winrate == None:
                if node.next != None:
                    raise Exception("no winrate during main line")
            else:
                winrates.append(winrate)
        node = node.next
    return winrates

def process(sgf_path: str) -> str:
    with open(sgf_path) as f:
        collection = sgf.parse(f.read())
    for game in collection:
        properties = game.root.properties
        result = [sgf_path, properties.get("DT",[""])[0], properties.get("PB",[""])[0], properties.get("PW",[""])[0], properties.get("RE",[""])[0]]
        result = list(map(lambda e: '"' + e + '"', result))
        try:
            result += list(map(lambda e: str(e), winrates_of(game)))
        except Exception as e:
            result.append("\"invalid sgf\"")
        return ",".join(result)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} <directory>".format(sys.argv[0]))
        sys.exit(0)
    print("path,date,b_player_name,w_player_name,result,winrates")
    with Pool(psutil.cpu_count(logical=False)) as pool:
        for e in pool.imap_unordered(process, file_pathes_under(sys.argv[1], "sgf"), 1):
            print(e)
