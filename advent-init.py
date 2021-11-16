import requests
from pathlib import Path, PosixPath
import sys
import datetime
import argparse
import itertools
import traceback
import logging
import shutil

# url = f"https://adventofcode.com/{year}/day/{day}/input"

logging.basicConfig(level=logging.DEBUG)
root = Path(sys.modules['__main__'].__file__).resolve().parent
secrets_path = Path(root, "secrets")
source = Path(root, "source")

badstr = "Puzzle inputs differ by user.  Please log in to get your puzzle input."

def create_directory(dir: PosixPath) -> None:
    # Generate source if not exist
    logging.debug(f"Creating new directory.\n -> {dir.as_posix()}")
    if not dir.is_dir():
        try:
            dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            logging.debug(f"It ok! Path exists.\n -> {dir.as_posix()}")
        else:
            logging.info(f"Created new directory.\n -> {dir.as_posix()}")

def get_remote_content(url: str, cookie: str = "") -> str:
    if cookie:
        payload = {"cookie": f"session={cookie}"}
        try:
            r = requests.get(url, headers=payload)
        except Exception as e:
            # a lot can go wrong here
            logging.exception(f"Something went terribly wrong!\n -> {e}\n{traceback.format_exc()}")
    else:
        try:
            r = requests.get(url)
        except Exception as e:
            logging.exception(f"Something went terribly wrong!\n -> {e}\n{traceback.format_exc()}")
    logging.debug(f"Got data from the following url.\n -> {url}")
    return r.content.decode("utf-8")

def get_day_range(day: str) -> list:
    r = [str(x).zfill(2) for x in range(1, int(day) + 1)]
    logging.debug(f"Got the following day range.\n -> {r}")
    return r

def create_missing_days(year: str, day: str) -> list:
    all_days_to_date = [Path(source, year, str(x)) for x in get_day_range(day)]
    existing_day_paths = list(filter(Path.is_dir, Path(source, year).glob('[0-2][0-9]')))
    paths_to_create = [x for x in all_days_to_date if x not in existing_day_paths]

    logging.debug(f"These are the days we're missing.\n -> {[f'date: {x.parts[-2]}/{x.parts[-1]}' for x in paths_to_create]}")

    # Create the paths
    for path in paths_to_create:
        create_directory(path)
    
    return all_days_to_date

def get_cookie(cookie_path: str = ".cookie"):
    with open(Path(secrets_path, cookie_path).as_posix()) as f:
        cookie = f.read()
        logging.debug(f"Got a cookie to use.")
    if not cookie:
        logging.debug(f"Could not load cookie.")
        raise ValueError
    return cookie

def copy_missing_templates(path):
    # Is this the most complicated way? yes.
    # Is this something i'm doing for fun? yes
    files = ["part1.py", "part2.py"]
    paths = [Path(path, x) for x in files]
    files_to_create = [x for x in paths if not x.is_file()]
    logging.debug(f"These are the files we're missing.\n -> {[x.as_posix() for x in files_to_create]}")
    for file in files_to_create: 
        # as_posix returns as a valid path in windows, even tho you should feel shame for using windows
        src = Path(root, "templates", "main.py").as_posix()
        dst = file.as_posix()
        try:
            shutil.copy(src, dst)
            logging.debug(f"Copied a file.\n -> source: {src}\n -> destination: {dst}")
        except OSError as e:
            logging.exception(f"Failed to copy a file.\n -> source: {src}\n -> destination: {dst}")

def get_missing_input(path: Path, cookie: str):
    dst = Path(path, "input.txt")
    if dst.is_file():
        logging.debug(f"The file already exists.\n -> file: {dst}")
        pass
    year, day = path.parts[-2], path.parts[-1].strip("0")
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    with open(dst, "w") as f:
        content = get_remote_content(url, cookie)
        if content == badstr:
            logging.warning(f"There was an error getting the data.\n -> Cookie: {cookie}")
        f.write(content)
        logging.debug(f"Wrote content to file.\n -> file: {dst}")

def create_missing_files(list_of_paths):
    cookie = get_cookie()
    for path in list_of_paths:
        copy_missing_templates(path)
        get_missing_input(path, cookie)

def parse_args(argv):
    # https://docs.python.org/3/library/argparse.html

    # I could probably allow setting a custom source path...

    parser = argparse.ArgumentParser(description="Get day and year for advent.")
    parser.add_argument(
        "-y", 
        type=str,
        help="Specify the year to be used for the query."
    )
    parser.add_argument(
        "-d", 
        type=str,
        help="Specify the day to be used for the query."
    )
    args = parser.parse_args(argv)
    return args

def main(argv):
    """
    year: year in which we will opperate
    day: the last day of the month (or current date) max 25th
    """

    args = parse_args(argv)

    if args.y and args.d:
        year = args.y
        day = args.d
    elif datetime.datetime.now().strftime("%m") == '12':
        year = datetime.datetime.now().strftime("%Y")
        day = datetime.datetime.now().strftime("%d")
    else:
        print("The current date either needs to be in december before the 26th or you need to specify the date via -y and -d.")
        quit()

    # Setup the dirs up to the specified date for the year
    all_days = create_missing_days(year, day)
    
    # Create the missing files for all days
    create_missing_files(all_days)

if __name__ == "__main__":
    main(sys.argv[1:])
