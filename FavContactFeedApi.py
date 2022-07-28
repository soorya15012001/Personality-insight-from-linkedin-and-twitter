import json

import tweepy
from bson import ObjectId

import config
from pymongo import MongoClient

client = MongoClient("mongodb+srv://soorya:soor1234@cluster0.jt4dn.mongodb.net/R_model?retryWrites=true&w=majority",
                     connect=False)
db = client.get_database("R_model")
r = db.FavContactFeed

client = tweepy.Client(config.BEARER)

from datetime import datetime
import requests
from urllib.parse import urlencode
import endpoint_1 as e
import get_twitter as gt
import config

headers = {}


def get_between(s):
    start = 'Response(data=<User id=;'
    end = ' name='
    r = s[s.find(start) + len(start):s.rfind(end)]
    return r


def get_tweets(tid, id):
    t = client.get_users_tweets(id=id, max_results=100, tweet_fields=['created_at', 'lang', 'public_metrics'])
    tw = []
    for i in t.data:
        x = dict(i.public_metrics)
        x.update({"text": i.text, "id": i.id})
        tw.append(x)
    like = sorted(tw, key=lambda d: d['like_count'], reverse=True)
    cmt = sorted(tw, key=lambda d: d['reply_count'], reverse=True)
    retweet = sorted(tw, key=lambda d: d['retweet_count'], reverse=True)

    return {
        "most_liked": {"text": like[0]["text"], "url": "https://twitter.com/" + tid + "/status/" + str(like[0]["id"])},
        "most_comment": {"text": cmt[0]["text"], "url": "https://twitter.com/" + tid + "/status/" + str(cmt[0]["id"])},
        "most_retweet": {"text": retweet[0]["text"],
                         "url": "https://twitter.com/" + tid + "/status/" + str(retweet[0]["id"])},
    }


def linkedin_mosts(x):
    like = sorted(x, key=lambda d: d['num_like'], reverse=True)
    cmt = sorted(x, key=lambda d: d['num_cmt'], reverse=True)
    return {
        "most_liked": {"text": like[0]["post"], "time": like[0]["time_period"]},
        "most_comment": {"text": cmt[0]["post"], "time": cmt[0]["time_period"]},
    }


def index(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token):
    with requests.session() as s:
        print(csrf_token)
        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = csrf_token
        s.headers["csrf-token"] = csrf_token[1:-1]

        # s.cookies['li_at'] = "AQEDAR_lA9YB1PmDAAABfLgZXlcAAAF_xAyJcE0AL5d2VzWVHhwlKh4115KaUsC9aZOBBPEAeHEAQLkZe43naMeMIpizdj52ixHr1ZptjSuDt4lyY4WvGbWecqBJ58QbAMwpQTi7TpEJJ__lVLYWN4kM"
        # s.cookies["JSESSIONID"] = '"ajax:8251942653812622234"'
        # s.headers["csrf-token"] = "ajax:8251942653812622234"

        key = key_name.strip() + " " + key_company.strip() + " " + key_role.strip()

        if liu == "":
            return {"Enter LIU Handle"}

        if pub_id != "" or key != "":
            info = dict(e.index(pub_id, key, s))
            all = info.popitem()

        if pub_id == "" and key == "":
            info = {"linkedin_handle": "",
                    "linkedin_url": "",
                    "total_profiles": "",
                    "first_name": "",
                    "last_name": "",
                    "headline": "",
                    "about": "",
                    "location": {"city": "", "state": "", "country": ""},
                    "email": "",
                    "phone_number": "",
                    "twitter": "",
                    "twitter_url": "",
                    "companies": "",
                    "latest_linkedin_post": "",
                    "schools": ""}

        tid = ""
        if twitter_id == "":
            tid = info["twitter"]
            if tid != "":
                print("no twitter id given. ID retrieved =", tid)
                twitter = gt.main_t(tid)
                latest_tweet = twitter["tweet"]
                t_info = twitter["info"]
            else:
                print("No twitter id given. No twitter from Linkedin extracted")
                latest_tweet = {"tweet_url": "", "tweet_text": "", "tweet_date": ""}
                t_info = {"name": "", "about": "", "img": "", "loc": ""}
        else:
            print("twitter id given. ID =", twitter_id)
            tid = twitter_id
            twitter = gt.main_t(twitter_id)
            latest_tweet = twitter["tweet"]
            t_info = twitter["info"]

        # print(info)

        try:
            u = client.get_user(username=tid)
            f_id = get_between(str(u))
            tw_most = get_tweets(tid, f_id)
        except:
            tw_most = {
                "most_liked": {"text": "", "url": ""},
                "most_comment": {"text": "", "url": ""},
                "most_retweet": {"text": "", "url": ""},
            }
        print(info)
        final = {"current_date_time": datetime.now(),
                 "email": info["email"],
                 "first_name": info["first_name"],
                 "last_name": info["last_name"],
                 "image": t_info["img"],
                 "linkedin_handle": info["linkedin_handle"],
                 "twitter_handle": tid,
                 "tweet": latest_tweet["tweet_text"],
                 "tweet_date": latest_tweet["tweet_date"],
                 "tweet_url": latest_tweet["tweet_url"],
                 "linkedin_post": info["latest_linkedin_post"]["post"],
                 "linkedin_date": info["latest_linkedin_post"]["time_period"],
                 "linkedin_url": info["latest_linkedin_post"]["url"],
                 "current_company": list(info["companies"][0].values())[0],
                 "company_change": False,
                 "twitter_most": tw_most,
                 "linkedin_most": linkedin_mosts(all[1]),
                 "request_by": req_by
                 }

        return final



new = index(liu = "sudipdutta", req_by="Sudip Dutta", pub_id="", key_name="Sudip Dutta", key_company="Relatas", key_role="", twitter_id="", li_at="AQEDASFwZlIBKM0RAAABgIQVgaQAAAGAqCIFpE0AdQX0lWQPkobU2Vc8IgWy-XOoMuSDXOhfv-bPjn4S3C8RUfO2bcQmpNRFwnMXWq5Bqgt6AFjQejtUTM3zIHyk4jsHy0iS0ovJ5pR5Wb9HES-l9HmF", csrf_token="\"ajax:5523655984287776427\"")
myquery = {"linkedin_handle": new["linkedin_handle"]}
comp = new["current_company"]

try:
    if comp != dict(r.find_one({"linkedin_handle": new["linkedin_handle"]}))["current_company"]:
        newvalues = {"$set": {"company_change": True, "current_company": new["current_company"]}}
    else:
        newvalues = {"$set": {"company_change": False}}
    r.update_one(myquery, newvalues)

except:
    r.insert_one(new)

for x in r.find():
    print(x)