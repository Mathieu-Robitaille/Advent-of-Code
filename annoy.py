
# YOU HAVENT DONE THE DAY"S WORK YET.
# GET BACK TO WORK.

# This is meant to be shit and quick.

import json
from twilio.rest import Client
from pathlib import Path
import sys
import datetime
import requests

root = Path(sys.modules["__main__"].__file__).resolve().parent
twilio_file = Path(root, "secrets", ".twilio")
cookie_file = Path(root, "secrets", ".cookie")
year = datetime.datetime.now().strftime("%Y")
month = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")

def time_to_annoy(message_body: str = "DO TODAY'S ADVENT."):
    with open(twilio_file) as f:
        secrets = json.load(f)
        client = Client(secrets["account_sid"], secrets["token"])
        client.messages \
            .create(
                body=message_body,
                from_=secrets["src_number"],
                to=secrets["dst_number"]
            )

if month != "12" or int(day) > 25:
    print("Sheeeeeeit.... Let santa sleep fam.")
    quit()

todays_challenge_path = Path(root, "source", year, day)

if not todays_challenge_path.is_dir():
    time_to_annoy(f"Bruh, you haven't even started... its fuckin {datetime.datetime.now().strftime('%H:%M:%S')} get goin u beesh.")
    quit()

is_complete_str = "Both parts of this puzzle are complete!"

with open(cookie_file) as f:
    cookie = f.read()
    url = f"https://adventofcode.com/{year}/day/{day}"
    payload = {"cookie": f"session={cookie}"}
    r = requests.get(url, headers=payload)
    result = r.content.decode('utf-8')
    if is_complete_str not in result:
        time_to_annoy("I cannot believe you've done this. Finish it faster you ape.")
    else:
        print("Good :)")

