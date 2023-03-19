import newspaper
import requests
import time


def get_articles(url, site_name, token, ch_uname):
    paper = newspaper.build(url, memoize_articles=True)

    for article in paper.articles:
        article.download()
        article.parse()
        article.nlp()
        params = {'chat_id': ch_uname,
                  'parse_mode': 'html',
                  "reply_markup": {
                      "inline_keyboard": [
                          [{"text": "Read Full Article", "url": ""}, ]
                      ]
                  }
                  }

        bot_url = f'https://api.telegram.org/bot{token}/sendphoto'

        caption = '\n\n'.join(
            [f"<b>{article.title} | {site_name}</b>", article.summary.replace('\n', ' ')[:250]+"[...]"])

        params.update({'caption': caption, 'photo': article.top_image})

        params['reply_markup']['inline_keyboard'][0][0]['url'] = article.url

        rsp = requests.post(bot_url, json=params)

        print(rsp.status_code)

        time.sleep(3)


def main_task(bot_token, sites):

    print("The main task has started execution")
    for s in sites:
        get_articles(s[0], s[1], bot_token, '@swenezt_test')
