# pylint: disable=protected-access
import pytest

from aoc2022.day_10 import CPU, parse_input

TEST_INPUT_1_STR = """
noop
addx 3
addx -5
""".strip()


@pytest.fixture(name="input_1")
def input_1_fixture():
    return [("noop", 0), ("addx", 3), ("addx", -5)]


@pytest.fixture(name="input_2")
def input_2_fixture():
    with open("./tests/data/day_10.txt", encoding="utf-8") as test_file:
        return parse_input(test_file.read())


def test_parse_input(input_1):
    assert parse_input(TEST_INPUT_1_STR) == input_1


def test_cpu_correctly_runs_test_input_1(input_1):
    cpu = CPU(cmds=input_1, init_reg_x=1)
    for _cmd in cpu.cmds:
        cpu.run_cmd(_cmd)
    print(cpu.reg_x_value)

    assert [v["during"] for k, v in cpu.reg_x_value.items() if k > 0] == [
        1,
        1,
        1,
        4,
        4,
        -1,
    ]


def test_cpu_method_compute_signal_strength_at_intervals(input_2):
    cpu = CPU(cmds=input_2, init_reg_x=1)
    for _cmd in input_2:
        cpu.run_cmd(_cmd)

    values_we_want = list(range(20, cpu.cycle, 40))
    good_cycle_vals = [cpu.reg_x_value[val]["during"] for val in values_we_want]
    assert good_cycle_vals == [21, 19, 18, 21, 16, 18]
