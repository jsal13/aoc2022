import os
from dataclasses import dataclass
from typing import List, Optional, Union

from aoc2022.utils import read_aoc_day_data_file

# TODO: Needs some Work.


def parse_process_list(input_stream) -> List[List[str]]:
    """Parse input data into commands."""
    current_line_idx = 0
    current_line = None
    parsed_commands_list = []
    cwd = ""
    process_list = list(input_stream.splitlines())
    while current_line_idx < len(process_list) - 1:
        current_line = process_list[current_line_idx]

        if current_line[0] == "$":
            # Line is a command.

            if current_line[2:4] == "cd":
                # Change directory...
                split_command = current_line.split(" ")
                cwd = os.path.abspath(os.path.join(cwd, split_command[2]))
                parsed_commands_list.append(split_command[1:3])

                current_line_idx += 1

            elif current_line[2:4] == "ls":
                # List directory...
                ls_cmd = ["ls", cwd]

                while (
                    current_line_idx < len(process_list) - 1
                    and process_list[current_line_idx + 1][0] != "$"
                ):
                    current_line_idx += 1
                    current_line = process_list[current_line_idx]
                    ls_cmd.append(current_line)

                parsed_commands_list.append(ls_cmd)
                current_line_idx += 1
            else:
                current_line_idx += 1
        else:
            raise ValueError("Should not be processing a non-command.")

    return parsed_commands_list


@dataclass
class File:
    """Represent a File which will have a name, extension, and size."""

    name: str
    extension: str
    size: int


@dataclass
class Directory:
    """Represent a directory which may contain other ``Directory``s and ``File``s."""

    name: str
    parent: Optional["Directory"]
    children: Optional[List[Union["Directory", File]]]


@dataclass
class FileSystem:
    """Represents the file system containing ``Directory``s and ``File``s."""

    dirs: List[Directory]

    def add_child_directory(self, target_dir: Directory):
        """Add directory to parent directory."""
        if target_dir.name not in [d.name for d in self.dirs if isinstance(d, Directory)]:
            self.dirs.append(target_dir)
            if target_dir.parent is not None and target_dir.parent.children is not None:
                target_dir.parent.children.append(target_dir)

    def add_file_to_directory(self, target_dir: Directory, file: File):
        """Add ``File`` to a ``Directory``."""
        if target_dir.children is not None:
            if file.name not in [f for f in target_dir.children if isinstance(f, File)]:
                target_dir.children.append(file)

    def get_dir_by_name(self, dirname: str) -> Directory:
        """Return ``Directory``with corresponding ``dirname``."""
        return [d for d in self.dirs if d.name == dirname][0]

    def calculate_dir_size(self, directory_name: str) -> int:
        """Calculate the size of a ``Directory`` given its name."""
        size = 0
        directory = self.get_dir_by_name(directory_name)
        if directory.children is not None:
            for item in directory.children:
                if isinstance(item, File):
                    size += item.size
                else:
                    size += self.calculate_dir_size(item.name)
        return size


def populate_file_system_from_cmds(data: str) -> FileSystem:
    """Populate the filesystem tree with Directories and Files given ``data`` commands."""
    parsed_cmds = parse_process_list(data)

    filesystem = FileSystem(dirs=[Directory(name="/", parent=None, children=[])])
    cwd = "/"
    for cmd in parsed_cmds:
        if cmd[0] == "cd":
            new_dir_loc = os.path.abspath(os.path.join(cwd, cmd[1]))
            new_dir = Directory(
                name=new_dir_loc, parent=filesystem.get_dir_by_name(cwd), children=[]
            )
            filesystem.add_child_directory(new_dir)
            cwd = new_dir_loc
        if cmd[0] == "ls":
            cwd = cmd[1]
            for item in cmd[2:]:
                if item[:4] != "dir ":
                    size, name = item.split(" ")
                    if "." in name:
                        name, ext = name.split(".")
                    else:
                        ext = ""
                    current_dir = filesystem.get_dir_by_name(cwd)
                    filesystem.add_file_to_directory(
                        current_dir, File(name=name, extension=ext, size=int(size))
                    )
    return filesystem


if __name__ == "__main__":
    problem_data = read_aoc_day_data_file(7)
    problem_filesystem = populate_file_system_from_cmds(problem_data)

    # Part 1
    total_p1: int = 0
    for d in [d for d in problem_filesystem.dirs if isinstance(d, Directory)]:
        dir_size = problem_filesystem.calculate_dir_size(d.name)
        if dir_size <= 100_000:
            total_p1 += dir_size
    print(f"Part 1: {total_p1}")

    # Part 2
    root_dir_size = problem_filesystem.calculate_dir_size("/")
    min_space_needed = -1 * ((70_000_000 - 30_000_000) - root_dir_size)
    possible_dirs_to_cut = []
    for d in [d for d in problem_filesystem.dirs if isinstance(d, Directory)]:
        dir_size = problem_filesystem.calculate_dir_size(d.name)
        if dir_size >= min_space_needed:
            possible_dirs_to_cut.append(dir_size)
    print(f"Part 2: {min(possible_dirs_to_cut)}")

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

    print(parse_process_list(COMMANDS_STR))
