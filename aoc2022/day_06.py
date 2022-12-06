from aoc2022.utils import read_aoc_day_data_file


def get_start_marker_index(stream: str, packet_size: int = 4) -> int:
    """Return the index of the start marker for ``stream``."""
    for idx in range(len(stream) - packet_size - 1):
        if len(set(stream[idx : idx + packet_size])) == packet_size:
            return idx + packet_size
    return -1


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(6)

    result = get_start_marker_index(raw_data)
    print(f"Part 1: {result}")

    result = get_start_marker_index(raw_data, packet_size=14)
    print(f"Part 2: {result}")
