# pylint: disable=protected-access
import pytest

from aoc2022.day_06 import get_start_marker_index

TEST_CASES_PART_1 = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]

TEST_CASES_PART_2 = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
]


@pytest.mark.parametrize("stream,expected", TEST_CASES_PART_1)
def test_get_start_marker_index_packet_size_4(stream, expected):
    assert get_start_marker_index(stream, packet_size=4) == expected


@pytest.mark.parametrize("stream,expected", TEST_CASES_PART_2)
def test_get_start_marker_index_packet_size_14(stream, expected):
    assert get_start_marker_index(stream, packet_size=14) == expected
