from typing import List

from aoc2022.utils import read_aoc_day_data_file


def get_total_calories_per_elf(data: str) -> List[int]:
    """Create list of calories carried by each elf."""
    list_per_elf_of_cals_strs = [elf_cals.split("\n") for elf_cals in data.split("\n\n")]
    elf_to_total_cals = [
        sum(map(int, elf_cals)) for elf_cals in list_per_elf_of_cals_strs
    ]
    return elf_to_total_cals


def get_total_calories_top_n(total_calorie_list: List[int], n: int) -> List[int]:
    """Return the top ``n`` values in the ``total_calorie_list``."""
    return sorted(total_calorie_list, reverse=True)[:n]


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(1)

    calorie_list = get_total_calories_per_elf(raw_data)

    print(f"Part 1: {sum(get_total_calories_top_n(calorie_list, 1))}")
    print(f"Part 2: {sum(get_total_calories_top_n(calorie_list, 3))}")
