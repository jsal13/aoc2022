# pylint: disable=protected-access
import pytest

from aoc2022.day_09 import RopeGrid, parse_cmds

TEST_DATA_1 = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()

TEST_DATA_2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip()


@pytest.fixture(name="test_data_1_cmds")
def test_data_1_cmds_fixture():
    return [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]


@pytest.fixture(name="test_data_2_cmds")
def test_data_2_cmds_fixture():
    return [
        ("R", 5),
        ("U", 8),
        ("L", 8),
        ("D", 3),
        ("R", 17),
        ("D", 10),
        ("L", 25),
        ("U", 20),
    ]


@pytest.fixture(name="ropegrid_1_knot_5x5")
def ropegrid_1_knot_5x5_fixture():
    return RopeGrid(start_loc=[2, 2], num_knots=2, grid_size=5)


def test_parse_cmds(test_data_1_cmds, test_data_2_cmds):
    assert parse_cmds(TEST_DATA_1) == test_data_1_cmds

    assert parse_cmds(TEST_DATA_2) == test_data_2_cmds


# This is the testing grid.  I'm sorry it's so gross.
#
# 1 a x b 2
# g . . . c
# w . T . y
# h . . . d
# 3 e z f 4

# TODO: Test 1, 2, 3, 4.


def test_class_ropegrid_move_head_at_x(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("U")
    ropegrid_1_knot_5x5.move("U")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [0, 2]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [1, 2]


def test_class_ropegrid_move_head_at_z(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("D")
    ropegrid_1_knot_5x5.move("D")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [4, 2]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [3, 2]


def test_class_ropegrid_move_head_at_w(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("L")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [2, 0]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 1]


def test_class_ropegrid_move_head_at_y(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("R")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [2, 4]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 3]


def test_class_ropegrid_move_head_at_a(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("U")
    ropegrid_1_knot_5x5.move("U")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [0, 1]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [1, 1]


def test_class_ropegrid_move_head_at_b(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("U")
    ropegrid_1_knot_5x5.move("U")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [0, 3]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [1, 3]


def test_class_ropegrid_move_head_at_c(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("U")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [1, 4]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 3]


def test_class_ropegrid_move_head_at_d(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("D")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [3, 4]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 3]


def test_class_ropegrid_move_head_at_e(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("D")
    ropegrid_1_knot_5x5.move("D")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [4, 1]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [3, 1]


def test_class_ropegrid_move_head_at_f(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("R")
    ropegrid_1_knot_5x5.move("D")
    ropegrid_1_knot_5x5.move("D")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [4, 3]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [3, 3]


def test_class_ropegrid_move_head_at_g(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("U")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [1, 0]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 1]


def test_class_ropegrid_move_head_at_h(ropegrid_1_knot_5x5):
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("L")
    ropegrid_1_knot_5x5.move("D")
    assert ropegrid_1_knot_5x5.knots_locs[0] == [3, 0]
    assert ropegrid_1_knot_5x5.knots_locs[1] == [2, 1]


def test_ropegrid_correctly_returns_total_tail_locs_for_test_data_1_cmds_2_knots(
    test_data_1_cmds,
):
    ropegrid = RopeGrid(start_loc=[25, 25], num_knots=2, grid_size=50)

    for cmd in test_data_1_cmds:
        for _ in range(cmd[1]):
            ropegrid.move(cmd[0])

    assert len(ropegrid.points_visited_by_knots[1]) == 13


def test_ropegrid_correctly_returns_total_tail_locs_for_test_data_1_cmds_10_knots(
    test_data_1_cmds,
):
    ropegrid = RopeGrid(start_loc=[25, 25], num_knots=10, grid_size=50)

    for cmd in test_data_1_cmds:
        for _ in range(cmd[1]):
            ropegrid.move(cmd[0])

    assert len(ropegrid.points_visited_by_knots[9]) == 1


def test_ropegrid_correctly_returns_total_tail_locs_for_test_data_2_cmds_10_knots(
    test_data_2_cmds,
):
    ropegrid = RopeGrid(start_loc=[25, 25], num_knots=10, grid_size=50)

    for cmd in test_data_2_cmds:
        for _ in range(cmd[1]):
            ropegrid.move(cmd[0])

    assert len(ropegrid.points_visited_by_knots[9]) == 36
