#!/usr/bin/env python3
import json
import urllib.request
import os
import re
import sys

TRELLO_KEY = os.environ.get("TRELLO_API_KEY", "13f24d5fc04deaf19fb1629c6d21e3f4")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN", "ATTA1ffe73ca57a9e96f98cc48af45062f0b4e1d4caa6339153c8ab74634450dcc3f2D682B73")
BOARD_ID = "6af3491a15ab3c1f1efcdaeb"

def get_all_cards():
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/cards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching cards from board: {e}", file=sys.stderr)
        return []

def get_next_it_id():
    cards = get_all_cards()
    max_id = 0
    pattern = re.compile(r"\[IT-(\d+)\]", re.IGNORECASE)
    for card in cards:
        name = card.get("name", "")
        match = pattern.search(name)
        if match:
            num = int(match.group(1))
            if num > max_id:
                max_id = num
    next_id = max_id + 1
    return f"IT-{next_id:02d}"

if __name__ == "__main__":
    next_tag = get_next_it_id()
    print(next_tag)
