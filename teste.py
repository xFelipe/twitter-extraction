import json 
import os
from requests import get
from dotenv import load_dotenv

load_dotenv()

auth_token = os.environ["AUTH_TOKEN"]
header = {"Authorization": "Bearer "+auth_token}
params = {
    "query": "Lula",
    "tweet.fields": "author_id,text,geo,id,in_reply_to_user_id,lang",
    "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id",
    "start_time": "2022-10-05T00:00:00z",
    "end_time": "2022-10-07T23:59:59z",
    "max_results": 10
}  # non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, source, withheld)

res = get("https://api.twitter.com/2/tweets/search/recent", params=params, headers=header)
print(res)
response_json = json.dumps(res.json())

with open("result.json", "w") as f:
    f.write(response_json)
