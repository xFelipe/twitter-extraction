import json
import os
from requests import get, Response
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from logging import Logger, INFO

logger = Logger(name=__name__, level=INFO)
logger.setLevel(INFO)
load_dotenv()


def __validate_response(response: Response):
    if response.status_code != 200:
        logger.error(response.json().get("errors"))
    else:
        logger.info(response)
    response.raise_for_status()


def __get_header():
    auth_token = os.environ["AUTH_TOKEN"]
    return {"Authorization": "Bearer "+auth_token}


def __paginate(next_token: str, query: str):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&next_token={next_token}"
    
    res = get(url, headers=__get_header())
    __validate_response(res)

    response_json = json.dumps(
        res.json(), ensure_ascii=False).encode('utf-8').decode()

    yield response_json

    next_token = res.json().get("meta", {}).get("next_token", "")
    if (next_token):
        yield from __paginate(next_token, query)


def search_tweets(query: str, dt: date = None):
    search_date = dt or (datetime.now() - timedelta(days=1))
    params = {
        "query": query,
        "tweet.fields": "author_id,text,geo,id,in_reply_to_user_id,lang,created_at,conversation_id",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id",
        "start_time": f"{search_date.year}-{search_date.month}-{search_date.day}T00:00:00z",
        "end_time": f"{search_date.year}-{search_date.month}-{search_date.day}T23:59:59z",
        "max_results": 10
    }  # non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, source, withheld)

    res = get("https://api.twitter.com/2/tweets/search/recent",
              params=params, headers=__get_header())
    __validate_response(res)

    response_json = json.dumps(
        res.json(), ensure_ascii=False).encode('utf-8').decode()

    yield response_json

    next_token = res.json().get("meta", {}).get("next_token", "")
    if (next_token):
        yield from __paginate(next_token, query)


if __name__ == "__main__":
    with open("result.json", "w") as f:
        for result in search_tweets("Lula"):
            f.write(result)
            break
