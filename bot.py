# bot.py
import os
import time
import pathlib
import random
import tweepy

API_KEY = os.environ["X_API_KEY"]
API_SECRET = os.environ["X_API_SECRET"]
ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")  # not used in free-schedule mode

STATE_DIR = pathlib.Path("state")
STATE_DIR.mkdir(exist_ok=True)
SINCE_PATH = STATE_DIR / "since_id.txt"  # kept for future upgrade
UID_PATH = STATE_DIR / "user_id.txt"     # kept for future upgrade

# OAuth 1.0a user context
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
)

def _read(p: pathlib.Path):
    try:
        return p.read_text().strip()
    except FileNotFoundError:
        return None

def _write(p: pathlib.Path, val: str):
    p.write_text(str(val).strip())

def get_my_user_id():
    # Use the authenticated account (no username lookup)
    me = client.get_me()
    return me.data.id

def main():
    my_id = get_my_user_id()
    print("Authenticated as user id:", my_id)

    # --- Free-tier mode: post a simple scheduled tweet and exit ---
    LINES = ["hi", "hello 👋", "sup", "yo", "hey there"]
    try:
        msg = random.choice(LINES)
        client.create_tweet(text=msg)
        print("Posted a scheduled tweet:", msg)
    except Exception as e:
        print("ERROR posting tweet:", repr(e))
        raise

    return  # end early (mentions reading is blocked on free tier)

if __name__ == "__main__":
    main()
