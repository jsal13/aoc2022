# pylint: disable=protected-access
import pytest

from aoc2022.day_08 import TreeGrid, parse_input

TREE_AS_STRING = """
30373
25512
65332
33549
35390
""".strip()

TREE_AS_MATRIX = [
    [3, 0, 3, 7, 3],
    [2, 5, 5, 1, 2],
    [6, 5, 3, 3, 2],
    [3, 3, 5, 4, 9],
    [3, 5, 3, 9, 0],
]


@pytest.fixture(name="tree_grid")
def tree_grid_fixture() -> TreeGrid:
    return TreeGrid(TREE_AS_MATRIX)


def test_parse_input():
    assert parse_input(TREE_AS_STRING) == TREE_AS_MATRIX


def test_case_treegrid_size_is_correct(tree_grid):
    assert tree_grid.size == 5


VISIBLE_TREES = (
    [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)]
    + [(0, col) for col in range(0, 5)]
    + [(4, col) for col in range(0, 5)]
    + [(row, 0) for row in range(0, 5)]
    + [(row, 4) for row in range(0, 5)]
)

NON_VISIBLE_TREES = [
    (row, col)
    for row in range(0, 5)
    for col in range(0, 5)
    if (row, col) not in VISIBLE_TREES
]


@pytest.mark.parametrize("row,col", VISIBLE_TREES)
def test_class_treegrid_method_is_visible_identifies_visible_trees(
    row, col, tree_grid: TreeGrid
):
    assert tree_grid.is_visible(row=row, col=col)


@pytest.mark.parametrize("row,col", NON_VISIBLE_TREES)
def test_class_treegrid_method_is_visible_identifies_non_visible_trees(
    row, col, tree_grid: TreeGrid
):
    assert not tree_grid.is_visible(row=row, col=col)


def test_class_treegrid_method_is_visible_correct_on_boundary(tree_grid: TreeGrid):
    for row in [0, tree_grid.size - 1]:
        for col in [0, tree_grid.size - 1]:
            assert tree_grid.is_visible(row=row, col=col)


def test_class_treegrid_method_count_val(tree_grid: TreeGrid):
    assert tree_grid.count_visible() == 21


TREES_VISIBLE = [(1, 2, [1, 1, 2, 2]), (3, 2, [2, 2, 1, 2])]


@pytest.mark.parametrize("row,col,expected", TREES_VISIBLE)
def test_class_treegrid_method_num_trees_visible(row, col, expected, tree_grid: TreeGrid):
    assert tree_grid.num_trees_visible(row=row, col=col) == expected
