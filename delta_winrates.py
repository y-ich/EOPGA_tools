"""
outputs the positions with AI's wonderful suggestions and professionals' execellent play moves.
"""
__author__ = "ICHIKAWA, Yuji <ichikawa.yuji@gmail.com>"

import sys
import csv
from typing import Tuple, Dict
import numpy as np
import sgf
from utilities import parse_comment

def get_delta_winrates(filename: str) -> Tuple[list[float], Dict[int, str]]:
    delta_winrates = []
    file_indices = {}
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # remove header
        for items in reader:
            file_indices[len(delta_winrates)] = items[0]
            black_winrates = list(map(lambda x: float(x), items[5:]))
            delta_black_winrates = map(lambda e: e[1] - e[0], zip(black_winrates, black_winrates[1:]))
            delta_winrates += list(map(lambda t: t[1] if t[0] % 2 == 0 else -t[1], enumerate(delta_black_winrates)))
    return delta_winrates, file_indices

def main(filename: str) -> None:
    delta_winrates, file_indices = get_delta_winrates(filename)
    indices = np.argsort(delta_winrates)
    print("AI's suggestion")
    count = 0
    for idx in indices:
        file_index = 0
        sgf_filename = file_indices[file_index]
        for i in file_indices:
            if i <= idx:
                file_index = i
                sgf_filename = file_indices[i]
            else:
                break
        with open(sgf_filename) as f:
            collection = sgf.parse(f.read())
        move_number = idx - file_index + 1
        n = 0
        for node in collection[0].rest:
            if "B" in node.properties or "W" in node.properties:
                n += 1
                if n == move_number:
                    winrate, visits = parse_comment(node.properties["C"][0])
                    if visits >= 800:
                        print(sgf_filename, move_number, delta_winrates[idx])
                        count += 1
                        break
        if count >= 10:
            break

    print("surprising move")
    for idx in indices[::-1]:
        if delta_winrates[idx] < 0.5:
            break
        file_index = 0
        sgf_filename = file_indices[file_index]
        for i in file_indices:
            if i <= idx:
                file_index = i
                sgf_filename = file_indices[i]
            else:
                break
        print(sgf_filename, idx - file_index + 1, delta_winrates[idx])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} <csv>".format(sys.argv[0]))
        sys.exit(0)
    main(sys.argv[1])
