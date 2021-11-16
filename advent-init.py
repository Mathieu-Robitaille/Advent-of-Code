from pathlib import Path, PosixPath
import argparse
import datetime
import logging
import requests
import shutil
import sys
import traceback

# Auto formatted by autopep8

# We need the root path incase your current working dir is different.
ROOT_PATH = Path(sys.modules['__main__'].__file__).resolve().parent

SECRETS_PATH = Path(ROOT_PATH, "secrets").absolute()
COOKIE_PATH = Path(SECRETS_PATH, ".cookie")

TEMPLATES_PATH = Path(ROOT_PATH, "templates").absolute()

badstr = "Puzzle inputs differ by user.  Please log in to get your puzzle input."


def create_directory(dir: PosixPath) -> None:
    # Generate source if not exist
    logging.debug(f"Creating new directory.\n -> {dir.as_posix()}")
    if not dir.is_dir():
        try:
            dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            # Not really going to end up here...
            logging.debug(f"It ok! Path exists.\n -> {dir.as_posix()}")
        else:
            logging.info(f"Created new directory.\n -> {dir.as_posix()}")


def get_remote_content(url: str, cookie: str) -> str:
    if cookie:
        payload = {"cookie": f"session={cookie}"}
        try:
            r = requests.get(url, headers=payload)
        except Exception as e:
            # a lot can go wrong here
            logging.exception(
                f"Something went terribly wrong!\n -> {e}\n{traceback.format_exc()}")
    else:
        try:
            r = requests.get(url)
        except Exception as e:
            logging.exception(
                f"Something went terribly wrong!\n -> {e}\n{traceback.format_exc()}")
    logging.debug(f"Got data from the following url.\n -> {url}")
    return r.content.decode("utf-8")


def get_day_range(day: str) -> list:
    r = [str(x).zfill(2) for x in range(1, int(day) + 1)]
    logging.debug(f"Got the following day range.\n -> {r}")
    return r


def create_missing_days(source: Path, year: str, day: str) -> list:
    all_days_to_date = [Path(source, year, str(x)) for x in get_day_range(day)]
    existing_day_paths = list(
        filter(Path.is_dir, Path(source, year).glob('[0-2][0-9]')))
    paths_to_create = [
        x for x in all_days_to_date if x not in existing_day_paths]

    logging.debug(
        f"These are the days we're missing.\n -> {[f'date: {x.parts[-2]}/{x.parts[-1]}' for x in paths_to_create]}")

    # Create the paths
    for path in paths_to_create:
        create_directory(path)

    return all_days_to_date


def get_cookie():
    with open(COOKIE_PATH) as f:
        cookie = f.read()
        logging.debug(f"Got a cookie to use.")
    if not cookie:
        logging.debug(f"Could not load cookie.")
        raise ValueError
    return cookie


def copy_missing_templates(challenge_code_path):
    # Is this THE most complicated way? yes. (without recursion and manually copying files)
    # Is this something I'm doing for fun? yes

    # Get all objects from the generator
    objects = [x for x in TEMPLATES_PATH.glob('**/*')]

    # We want to ommit the path to the templates part and re-construct the dir tree elsewhere
    ommit = len(TEMPLATES_PATH.parts)

    # Get each dir to pass, this already returns the deepest dir so we're not worried about wasting time on parents.
    directories_to_create = [
        Path(challenge_code_path, *x.parts[ommit:]) for x in objects if x.is_dir()
    ]

    # Create a tuple of src and dst
    files_to_create = [
        (x, Path(challenge_code_path, *x.parts[ommit:])) for x in objects if x.is_file()
    ]

    logging.debug(f"Creating directory structure from template.")
    for dir in directories_to_create:
        create_directory(dir)

    logging.debug(f"Copying files over to new structure.")
    for file in files_to_create:
        # as_posix returns as a valid path in windows, even tho you should feel shame for using windows
        src = file[0].as_posix()
        dst = file[1].as_posix()
        try:
            shutil.copy(src, dst)
            logging.debug(
                f"Copied a file.\n -> source: {src}\n -> destination: {dst}")
        except OSError:
            logging.exception(
                f"Failed to copy a file.\n -> source: {src}\n -> destination: {dst}")


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
            logging.warning(
                f"There was an error getting the data.\n -> Cookie: {cookie}")
        f.write(content)
        logging.debug(f"Wrote content to file.\n -> file: {dst}")


def user_warning(source, year):
    path = Path(source, year).as_posix()
    while True:
        inp = input(f"We're about to write to {path}\n\t - Is this ok? (y/N)")
        if inp in ["", "", "n", "N"]:
            logging.critical(f"Breaking out, {path} is a bad path.")
            quit()
        elif inp in ["y", "Y"]:
            logging.debug(f"Using {path}")
            break


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Get day and year for advent.")
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
    parser.add_argument(
        "-s",
        type=str,
        default=Path(ROOT_PATH, "source"),
        help="The directory in which you would like to build your proj relative (or absolute) to this file."
    )
    parser.add_argument(
        "-v",
        action='store_true',
        help="Verbose mode. Logging is set to debug (very loud)"
    )
    parser.add_argument(
        "-i",
        action='store_true',
        help="Confirm before starting"
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

    source = Path(args.s).absolute()

    # Just make super sure the user wants to do this
    if args.i:
        user_warning(source, year)

    if args.v:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cookie = get_cookie()
    for path in create_missing_days(source, year, day):
        copy_missing_templates(path)
        get_missing_input(path, cookie)


if __name__ == "__main__":
    main(sys.argv[1:])
