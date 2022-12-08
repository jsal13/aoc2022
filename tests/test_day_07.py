# pylint: disable=protected-access
# import pytest

from aoc2022.day_07 import (
    parse_process_list,  # FileSystem, populate_file_system_from_cmds
)

# TODO: MORE TESTS


COMMANDS_STR = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".strip()

COMMANDS_LIST = [
    ["cd", "/"],
    ["ls", "/", "dir a", "14848514 b.txt", "8504156 c.dat", "dir d"],
    ["cd", "a"],
    ["ls", "/a", "dir e", "29116 f", "2557 g", "62596 h.lst"],
    ["cd", "e"],
    ["ls", "/a/e", "584 i"],
    ["cd", ".."],
    ["cd", ".."],
    ["cd", "d"],
    ["ls", "/d", "4060174 j", "8033020 d.log", "5626152 d.ext", "7214296 k"],
]


def test_parse_process_list_correctly_parses():
    assert parse_process_list(COMMANDS_STR) == COMMANDS_LIST
