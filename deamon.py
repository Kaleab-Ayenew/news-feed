from poster import main_task
import time
from dotenv import load_dotenv
import sys
import os
import json


mins = 1


def deamon():
    load_dotenv()
    BOT_TOKEN = os.getenv("NEWS_BOT_TOKEN", None)
    if not BOT_TOKEN:
        print("Please set the bot token as an enviroment variable.")
        sys.exit(1)

    with open(r"site_list.json", "r") as list_file:
        sites = json.loads(list_file.read())

    while True:
        main_task(BOT_TOKEN, sites)
        time.sleep(60*mins)


deamon()
