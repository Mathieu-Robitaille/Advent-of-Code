# Quality of life imports
from pathlib import Path
from sys import modules, path

# Quality of life, define the input file location
src = Path(modules['__main__'].__file__).resolve().parent
input_file_path = Path(src, "input.txt")

helper_location = Path(src, "..", "..", "helpers")
path.insert(1, helper_location.as_posix())
from timer import time_func

EXAMPLE_MODE = True
example_answer = 0
example = """"""

@time_func
def dayXXpart2init(src):
    pass

@time_func
def dayXXpart2solve():
    sol = 0
    print(f"Part 2 answer: {sol}")
    pass

def part2(src):
    dayXXpart2init(src)
    dayXXpart2solve()
    

if __name__ == "__main__":
    src = []

    if EXAMPLE_MODE:
        src = example.split("\n")
    else:
        with open(input_file_path) as f:
            for line in f.readlines():
                src.append(line.strip('\n'))
    part2(src)
