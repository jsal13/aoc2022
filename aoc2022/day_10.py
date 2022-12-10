from typing import Any, List

import numpy as np

from aoc2022.utils import read_aoc_day_data_file


def parse_input(data: str) -> List[Any]:
    """Parse input for Day 10."""
    raw_cmds = [line.split(" ") for line in data.splitlines()]

    cmds: List[Any] = []
    for cmd in raw_cmds:
        if cmd[0] == "noop":
            cmds.append((cmd[0], 0))
        elif cmd[0] == "addx":
            cmds.append((cmd[0], int(cmd[1])))
        else:
            raise ValueError(f"No such command: {cmd}")

    return cmds


class Screen:
    """Represent the CRT Screen for Day 10."""

    def __init__(self, register_values: dict[int, dict[str, int]]):
        self.screen = np.full(shape=(6, 40), fill_value=".")
        self.register_values = register_values
        self.current_cycle = 1

    def get_sprite_indices(self):
        return [
            self.register_values[self.current_cycle]["during"] - 1,
            self.register_values[self.current_cycle]["during"],
            self.register_values[self.current_cycle]["during"] + 1,
        ]

    def draw(self):
        current_row = (self.current_cycle - 1) // 40
        current_col = (self.current_cycle - 1) % 40
        if current_col in self.get_sprite_indices():
            self.screen[current_row][current_col] = "#"

    def iterate(self):
        self.draw()
        self.current_cycle += 1


class CPU:
    """Represent the CPU for Day 10."""

    def __init__(self, cmds: List[tuple[str, int]], init_reg_x: int = 1):
        self.cmds = cmds + [("noop", 0)]  # End in a no-op.
        self.cycle = 1

        self.reg_x_value: dict[int, dict[str, int]] = {
            0: {"start": init_reg_x, "during": init_reg_x, "end": init_reg_x}
        }

    def run_cmd(self, cmd: tuple[str, int]):
        """Run command ``cmd``."""
        if cmd[0] == "noop":
            self.reg_x_value[self.cycle] = {
                "start": self.reg_x_value[self.cycle - 1]["end"],
                "during": self.reg_x_value[self.cycle - 1]["end"],
                "end": self.reg_x_value[self.cycle - 1]["end"],
            }
            self.cycle += 1

        elif cmd[0] == "addx":
            self.reg_x_value[self.cycle] = {
                "start": self.reg_x_value[self.cycle - 1]["end"],
                "during": self.reg_x_value[self.cycle - 1]["end"],
                "end": self.reg_x_value[self.cycle - 1]["end"],
            }
            self.cycle += 1
            self.reg_x_value[self.cycle] = {
                "start": self.reg_x_value[self.cycle - 1]["end"],
                "during": self.reg_x_value[self.cycle - 1]["end"],
                "end": self.reg_x_value[self.cycle - 1]["end"] + cmd[1],
            }
            self.cycle += 1


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(10)
    _cmds = parse_input(raw_data)

    cpu = CPU(_cmds, init_reg_x=1)
    for _cmd in _cmds:
        cpu.run_cmd(cmd=_cmd)

    # Part 1.
    good_cycles = list(range(20, 240, 40))
    signal_strengths = [
        k * v["during"] for k, v in cpu.reg_x_value.items() if k in good_cycles
    ]
    print(f"Part 1: {sum(signal_strengths)}")

    # Part 2.
    screen = Screen(register_values=cpu.reg_x_value)

    for _ in range(240):
        screen.iterate()

    print("Part 2:")
    for line in screen.screen:
        print(" ".join(line))
