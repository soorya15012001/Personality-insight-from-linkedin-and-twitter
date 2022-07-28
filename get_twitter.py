import datetime
import json
from datetime import date
import tweepy
import config
import requests
from collections import Counter

client = tweepy.Client(config.BEARER)

def get_between(s):
    start = 'Response(data=<User id=;'
    end = ' name='
    r = s[s.find(start) + len(start):s.rfind(end)]
    return r

def get_tweets(pub_id, id):
    try:
        t = client.get_users_tweets(id=id, max_results=100, tweet_fields=['created_at', 'lang'])
        tweet = []
        text = ""
        try:
            co = 0
            for i in t.data:
                if co > 50:
                    break
                else:
                    # if (datetime.datetime.now() - i.created_at).days < 7:
                    #     continue
                    if ('@' not in i.text):
                        url = "https://twitter.com/"+pub_id+"/status/" + str(i.id).replace("\n", "")
                        txt = str(i.text).replace("\n", "")
                        dat = i.created_at
                        tweet.append({"tweet_url": url, "tweet_text": txt, "tweet_date": dat})
                        text = text + txt
                co = co + 1
        except TypeError:
            tweet = []
        if len(tweet) == 0:
            tweet.append({"tweet_url": "", "tweet_text": "", "tweet_date": ""})
            text = ""

        return tweet, text
    except tweepy.errors.HTTPException:
        tweet = [{"tweet_url": "", "tweet_text": "", "tweet_date": ""}]
        text = ""
        return tweet, text

def user_info(id):
    import requests
    from requests.structures import CaseInsensitiveDict

    url = "https://api.twitter.com/2/users/by/username/"+id+"?user.fields=id,created_at,name,username,protected,verified,withheld,profile_image_url,location,url,description,entities,pinned_tweet_id,public_metrics"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAADorZgEAAAAADVfqoUhHN8dC4kMLqWaWRKc1yy4%3Dy2i7xdA342F3qsxK4iUYQ0dCfRllrD6cYUisj0mtH04XBO7VXv"

    resp = requests.get(url, headers=headers)
    # print(json.loads(resp.text)["data"])

    try:
        name = json.loads(resp.text)["data"]["name"]
    except KeyError:
        name = ""

    try:
        about = json.loads(resp.text)["data"]["description"]
    except KeyError:
        about = ""

    try:
        img = json.loads(resp.text)["data"]["profile_image_url"]
    except KeyError:
        img = ""

    try:
        loc = json.loads(resp.text)["data"]["location"]
    except KeyError:
        loc = ""

    return {"handle": id.strip().lower(), "name": name, "about": about, "img": img, "loc": loc}




def get_topics_retweets(id):
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAADorZgEAAAAADVfqoUhHN8dC4kMLqWaWRKc1yy4%3Dy2i7xdA342F3qsxK4iUYQ0dCfRllrD6cYUisj0mtH04XBO7VXv',
    }
    params = (
        ('tweet.fields', 'context_annotations,entities'),
    )

    try:
        t = client.get_users_tweets(id=id, max_results=100, tweet_fields=['created_at', 'lang'])
        topic = []
        try:
            for i in t.data:
                if ('@' in i.text):
                    id = str(i.id)
                    response = requests.get("https://api.twitter.com/2/tweets/" + id, headers=headers, params=params)
                    r = response.json()
                    try:
                        for i in r["data"]["context_annotations"]:
                            topic.append(i["entity"]["name"])
                    except:
                        continue
        except TypeError:
            topic = []

        if len(topic) == 0:
            topic.append("")
    except tweepy.errors.HTTPException:
        topic = [""]

    fin = {}
    # print(sorted(dict(Counter(topic)).items(), key=lambda x: x[1], reverse=True))
    for i, j in dict(Counter(topic)).items():
        if j >= 2:
            fin[i] = j
    return fin

def get_topics_likes(id):
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAADorZgEAAAAADVfqoUhHN8dC4kMLqWaWRKc1yy4%3Dy2i7xdA342F3qsxK4iUYQ0dCfRllrD6cYUisj0mtH04XBO7VXv',
    }
    params = (
        ('tweet.fields', 'context_annotations,entities'),
    )
    l = client.get_liked_tweets(id=id, max_results=100)
    topics = []
    for i in l.data:
        id = str(i.id)
        response = requests.get("https://api.twitter.com/2/tweets/" + id, headers=headers, params=params)
        r = response.json()
        try:
            for i in r["data"]["context_annotations"]:
                topics.append(i["entity"]["name"])
        except:
            continue
    fin = {}
    # print(sorted(dict(Counter(topics)).items(), key=lambda x: x[1], reverse=True))

    for i,j in dict(Counter(topics)).items():
        if j >= 2:
            fin[i] = j
    return fin



def index(pub_id):
    print("PUB_ID - ", pub_id)
    if "Try other keywords" in pub_id:
        return {"tweet": {"tweet_url": "", "tweet_text": "", "tweet_date": ""}, "txt": "",
                "info": {"handle": "", "name": "", "about": "", "img": "", "loc": ""}, "all": 0}
    else:
        u = client.get_user(username=pub_id)
        id = get_between(str(u))

        # like = get_topics_likes(id)
        # retweet = get_topics_retweets(id)
        # like.update(retweet)
        tweet, txt = get_tweets(pub_id, id)
        info = user_info(pub_id)
        # print("TWEET", tweet)
        # print("TXT", txt)
        # print("INFO", info)

        if info["handle"] != "":
            return {"tweet": tweet[0], "txt": txt, "info": info, "all": len(tweet)}
        else:
            return {"tweet": {"tweet_url": "", "tweet_text": "", "tweet_date": ""}, "txt": "", "info": {"handle": "", "name": "", "about": "", "img": "", "loc": ""}, "all": 0}

def main_t(pub_id):
    if pub_id == "":
        return {"tweet": {"tweet_url": "", "tweet_text": "", "tweet_date": ""}, "txt": "", "info": {"handle": "", "name": "", "about": "", "img": "", "loc": ""}, "all": 0}
    else:
        x = index(pub_id)
        return x

# print(main_t("SudipDutta"))