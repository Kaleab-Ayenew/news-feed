import newspaper
import os
import sys
import json
import requests
from dotenv import load_dotenv
import time


with open(r"site_list.json", "r") as list_file:
    sites = json.loads(list_file.read())


def get_articles(url, site_name):
    paper = newspaper.build(url, memoize_articles=True)
    content = []
    for article in paper.articles:
        article.download()
        article.parse()
        article.nlp()
        content.append({'image': article.top_image, 'title': f"{article.title} | {site_name}",
                       'text': article.summary.replace('\n', ' ')[:250]+"[...]", 'link': article.url})
    return content


def post_to_telegram(url, site_name, token, ch_uname):
    print(f"Getting {url}")
    articles = get_articles(url, site_name)
    params = {'chat_id': ch_uname,
              'parse_mode': 'html',
              "reply_markup": {
                  "inline_keyboard": [
                      [{"text": "Read Full Article", "url": ""}, ]
                  ]
              }
              }
    bot_url = f'https://api.telegram.org/bot{token}/sendphoto'

    for a in articles:
        caption = '\n\n'.join([f"<b>{a.get('title')}</b>", a.get('text')])
        params.update({'caption': caption, 'photo': a.get('image')})
        params['reply_markup']['inline_keyboard'][0][0]['url'] = a.get(
            'link')
        # async with session.get(bot_url) as rsp:
        #     print(f"[{rsp.status}] for link {url}")
        #     js_rsp = await rsp.json()
        print(a.get("link"))
        rsp = requests.post(bot_url, json=params, verify=False)
        print(rsp.status_code)
        js_rsp = rsp.json()
        print(f"Posted: {js_rsp.get('title')}")
        time.sleep(3)


def main_task():
    global sites
    load_dotenv()
    BOT_TOKEN = os.getenv("NEWS_BOT_TOKEN", None)
    if not BOT_TOKEN:
        print("Please set the bot token as an enviroment variable.")
        sys.exit(1)

    print("The main task has started execution")
    proc_list = []
    arg_list = []
    # async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
    #     await asyncio.gather(*(post_to_telegram(
    #         s[0], s[1], BOT_TOKEN, '@swenezt_test', session) for s in sites))
    for s in sites:
        # arg_list.append((s[0], s[1], BOT_TOKEN, '@swenezt_test'))
        post_to_telegram(s[0], s[1], BOT_TOKEN, '@swenezt_test')
