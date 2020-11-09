"""
utitilies functions
"""
__author__ = "ICHIKAWA, Yuji <ichikawa.yuji@gmail.com>"

from typing import Generator
import os

def file_pathes_under(directory: str, extension: str) -> Generator[str, None, None]:
    dot_extension = "." + extension
    for name in os.listdir(directory):
        p = os.path.join(directory, name)
        if os.path.isdir(p):
            yield from file_pathes_under(p, extension)
        elif p.endswith(dot_extension):
            yield p

def parse_comment(s: str) -> tuple[float, int]:
    tokens = s.split("\n")
    if len(tokens) != 2:
        raise Exception("invalid string")
    return float(tokens[0]), int(tokens[1])
