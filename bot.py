# bot.py
import os, time, pathlib
import tweepy

API_KEY = os.environ["X_API_KEY"]
API_SECRET = os.environ["X_API_SECRET"]
ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]
BOT_USERNAME = os.environ["BOT_USERNAME"]  # no @

STATE_DIR = pathlib.Path("state")
STATE_DIR.mkdir(exist_ok=True)
SINCE_PATH = STATE_DIR / "since_id.txt"
UID_PATH = STATE_DIR / "user_id.txt"

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
    uid = _read(UID_PATH)
    if uid:
        return uid
    u = client.get_user(username=BOT_USERNAME)
    uid = u.data.id
    _write(UID_PATH, uid)
    return uid

def main():
    my_id = get_my_user_id()
    since_id = _read(SINCE_PATH)

    params = dict(max_results=100, tweet_fields=["author_id","created_at"])
    if since_id:
        params["since_id"] = since_id

    resp = client.get_users_mentions(my_id, **params)
    tweets = list(resp.data or [])
    tweets.sort(key=lambda t: int(t.id))  # oldest → newest

    last_seen = since_id
    for t in tweets:
        if t.author_id == my_id:
            last_seen = t.id
            continue
        client.create_tweet(text="hi", in_reply_to_tw
