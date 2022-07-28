import json
import time
from datetime import datetime
from random import shuffle
from keras.models import load_model
import pickle
from keras_preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import re
from collections import Counter
import nltk
from flask import Flask, request
import requests
from urllib.parse import urlencode
import endpoint_1 as e
import get_twitter as gt
import config
from pymongo import MongoClient

client = MongoClient("mongodb+srv://soorya:soor1234@cluster0.jt4dn.mongodb.net/R_model?retryWrites=true&w=majority")
db = client.get_database("R_model")
r = db.contactIntelligence

nltk.download('stopwords')
nltk.download('wordnet')

headers = {}

app = Flask(__name__)


def search_profile(key, s):
    default_params = {"count": "1", "filters": "List()", "origin": "GLOBAL_SEARCH_HEADER", "q": "all", "start": 0,
                      "queryContext": "List(spellCorrectionEnabled->true,relatedSearchesEnabled->true,kcardTypes->PROFILE|COMPANY)",
                      "keywords": key}
    search = 'https://www.linkedin.com/voyager/api/search/blended?' + urlencode(default_params, safe='(),')
    sea = s.get(search)
    sea = sea.json()
    try:
        id = sea["elements"][0]["elements"][0]["image"]["attributes"][0]["miniProfile"]["publicIdentifier"]
    except IndexError:
        return "Nothing"

    return {"id": id, "total_profiles": str(sea['metadata']['totalResultDisplayText']['text']).split()[0]}


def personal_info(public_id, s):
    complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
    profile = s.get(complete_profile)
    profile = profile.json()
    try:
        urn = profile["profile"]["miniProfile"]["dashEntityUrn"]
    except:
        urn = ""
    try:
        about = profile['profile']['summary']
    except:
        about = ""
    try:
        headline = profile['profile']['headline']
    except:
        headline = ""

    return {"urn": urn, "headline": headline.lower(), "about": about.lower()}


def jobs(public_id, s):
    try:
        complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
        profile = s.get(complete_profile)
        profile = profile.json()
        company = []

        for i in range(len(profile['positionGroupView']['elements'])):
            for j in range(len(profile['positionGroupView']['elements'][i]["positions"])):

                try:
                    c_about = profile['positionGroupView']['elements'][i]["positions"][j]["description"]
                except:
                    c_about = ""
                company.append(c_about.lower())
        if len(company) == 0:
            company.append("")
            return company
        else:
            return company
    except:
        return []


def education_info(public_id, s):
    try:
        complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
        profile = s.get(complete_profile)
        profile = profile.json()

        education = []
        for i in profile['educationView']['elements']:
            try:
                e_about = i["activities"]
            except:
                e_about = ""
            education.append(e_about.lower())

        if len(education) == 0:
            education.append("")
            return education
        else:
            return education
    except:
        return []


def education_name(public_id, s):
    try:
        complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
        profile = s.get(complete_profile)
        profile = profile.json()

        education = []
        for i in profile['educationView']['elements']:
            try:
                education.append(i["schoolName"])
            except:
                education.append("")

        if len(education) == 0:
            education.append("")
            return education
        else:
            return education
    except:
        return []


def skill_name(public_id, s):
    try:
        sk = "https://www.linkedin.com/voyager/api/identity/profiles/" + public_id + "/skills"
        sk = s.get(sk)
        sk = sk.json()["elements"]
        skills = []
        for i in sk:
            skills.append(i["name"])

        if len(skills) == 0:
            skills.append("")
            return skills
        else:
            return skills
    except:
        return []


def company_name(public_id, s):
    try:
        complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
        profile = s.get(complete_profile)
        profile = profile.json()
        company = []
        for i in range(len(profile['positionGroupView']['elements'])):
            try:
                company.append(profile['positionGroupView']['elements'][i]['miniCompany']["name"])
            except:
                company.append("")
        if len(company) == 0:
            company.append("")
            return company
        else:
            return company
    except:
        return []


def article_info(public_id, s):
    try:
        posts = "https://www.linkedin.com/voyager/api/identity/profiles/" + public_id + "/posts"
        posts = s.get(posts)
        posts = posts.json()

        post = []
        for i in posts["elements"]:
            post.append(i["contentText"]["text"])

        if len(post) == 0:
            post.append("")
            return post
        else:
            return post
    except:
        return []


def posts_info(urn, s):
    try:
        url_params = {
            "count": 100,
            "start": 0,
            "q": "memberShareFeed",
            "moduleKey": "member-shares:phone",
            "includeLongTermHistory": True,
        }
        profile_urn = urn
        url_params["profileUrn"] = profile_urn

        posts = "https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?" + urlencode(url_params, safe='(),')

        posts = s.get(posts)
        posts = posts.json()
        p = []
        for i in posts["elements"]:
            try:
                p.append(i["commentary"]["text"]["text"])
            except KeyError:
                continue

        if len(p) == 0:
            p.append("")
            return p
        else:
            return p
    except:
        return []


def ice_breaker(liu, public, public_id, s):
    xxx = e.index(pub_id=liu, key="", s=s)
    # xxy = e.index(pub_id=public_id, key="", s=s)

    liu_school = {x.lower(): x for x in education_name(liu, s)}
    liu_skill = {x.lower(): x for x in skill_name(liu, s)}
    liu_comp = {x.lower(): x for x in company_name(liu, s)}
    liu_city = xxx["location"]["city"]
    liu_state = xxx["location"]["state"]
    liu_country = xxx["location"]["country"]
    # liu_twitter = gt.main_t(liu)["topics"]
    # print(liu_twitter)

    c_school = {x.lower(): x for x in education_name(public_id, s)}
    c_skill = {x.lower(): x for x in skill_name(public_id, s)}
    c_comp = {x.lower(): x for x in company_name(public_id, s)}
    c_city = public["location"]["city"]
    c_state = public["location"]["state"]
    c_country = public["location"]["country"]
    # c_twitter = gt.main_t(public_id)["topics"]
    # print(c_twitter)

    c = ""
    s = ""
    co = ""

    uc = ""
    us = ""
    uco = ""

    if liu_city == c_city:
        c = liu_city
    else:
        uc = c_city
    if liu_state == c_state:
        s = liu_state
    else:
        uc = c_state
    if liu_country == c_country:
        co = liu_country
    else:
        uc = c_country

    school_ib = list(set(liu_school.keys()).intersection(c_school.keys()))
    skill_ib = list(set(liu_skill.keys()).intersection(c_skill.keys()))
    comp_ib = list(set(liu_comp.keys()).intersection(c_comp.keys()))
    # twitter_ib = list(set(liu_twitter).intersection(c_twitter))

    school_uib = list(set(c_school.keys()).difference(liu_school.keys()))
    skill_uib = list(set(c_skill.keys()).difference(liu_skill.keys()))
    comp_uib = list(set(c_comp.keys()).difference(liu_comp.keys()))
    # twitter_uib = list(set(c_twitter).difference(liu_twitter))

    # x = "uncommon_IB": {"school_IB": [liu_school[i] for i in school_ib], "skill_IB": [liu_skill[i] for i in skill_ib],
    #                       "company_IB": [liu_comp[i] for i in comp_ib],
    #                       "location_IB": {"city": c, "state": s, "country": co}, "twitter_topics": twitter_ib}

    return {"common_IB": {"school_IB": [liu_school[i] for i in school_ib], "skill_IB": [liu_skill[i] for i in skill_ib],
                          "company_IB": [liu_comp[i] for i in comp_ib],
                          "location_IB": {"city": c, "state": s, "country": co}},

            "uncommon_IB": {"school_IB": [c_school[i] for i in school_uib], "skill_IB": [c_skill[i] for i in skill_uib],
                            "company_IB": [c_comp[i] for i in comp_uib],
                            "location_IB": {"city": uc, "state": us, "country": uco}}
            }


def clean(s):
    maxlen = 1500
    trunc_type = "post"
    pad_type = "post"
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer_l = pickle.load(handle)
    lemmatizer = nltk.wordnet.WordNetLemmatizer()
    stop_words = stopwords.words('english')
    words = set(nltk.corpus.words.words())
    stopwords_dict = Counter(stop_words)
    s = s.lower()
    s = re.sub('<.*?>', '', s)
    s = re.sub('... See more', '', s)
    s = re.sub(r"http\S+", '', s)
    s = re.sub('[^A-Za-z0-9]+', ' ', s)
    s = re.sub("[0-9]", ' ', s)
    s = re.sub(" +", ' ', s)
    s = ' '.join([word for word in s.split() if word not in stopwords_dict])
    s = " ".join([lemmatizer.lemmatize(w) for w in s.split(' ')]).strip()
    s = " ".join(w for w in nltk.wordpunct_tokenize(s) if w.lower() in words or not w.isalpha() or len(w.lower()) > 2)
    data = [s]
    sequences = tokenizer_l.texts_to_sequences(data)
    padded = pad_sequences(sequences, maxlen=maxlen, truncating=trunc_type, padding=pad_type)
    return padded


def clean_name(s):
    s = s.lower()
    s = re.sub('<.*?>', '', s)
    s = re.sub(r'\\.*', "", s)
    s = re.sub(r'\-.*', "", s)
    s = re.sub('[\(\[].*?[\)\]]', "", s)
    s = s.strip()
    s = re.sub("[^a-zA-Z]+", "", s)
    return s


def get_detail(s, pub_info, liu="", pub_id="", key=""):
    id = {"id": "", "total_profiles": 1}
    if liu == "":
        return {"logged_in_user_handle": "Enter handle of logged in user"}

    if pub_id == '' and key != '':
        id = search_profile(key, s)

        if id == "Nothing":
            return ["enter some other keywords!"]

        pub_id = id["id"]

    elif pub_id == '' and key == '  ':
        return {"input_error": "enter profile handle or keywords!"}

    if pub_id == "try other keywords!!":
        return {"keyword_error": "enter some other keywords!"}

    personal = [personal_info(pub_id, s)["headline"], personal_info(pub_id, s)["about"]]
    company = jobs(pub_id, s)
    education = education_info(pub_id, s)
    article = article_info(pub_id, s)
    post = posts_info(personal_info(pub_id, s)["urn"], s)
    IB = ice_breaker(liu=liu, public=pub_info, s=s, public_id=pub_id)
    x = personal + company + post + education + article
    "".join(x)
    return [x, IB]


# @app.route('/dynamic/', methods=['GET'])
def dd(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token):
    with requests.session() as s:

        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = "\"" + csrf_token + "\""
        s.headers["csrf-token"] = csrf_token

        start = time.time()

        # liu = request.args['liu']
        # req_by = request.args['req_by']
        # pub_id = request.args['pub_id']
        # key_name = request.args['key']
        # key_company = request.args['comp']
        # key_role = request.args['role']
        # twitter_id = request.args['twitter_id']

        key = key_name.strip() + " " + key_company.strip() + " " + key_role.strip()

        if liu == "":
            tx = {"LIUerror": "Looks like your session has expired. Please logout and login again."}

        else:
            if pub_id != "" or key != "  ":
                print("pub_id-", pub_id)
                print("key-", key)

                if pub_id != "":
                    info = dict(e.index(pub_id=pub_id, key="", s=s))
                elif key != "  ":
                    info = dict(e.index(pub_id=pub_id, key=key, s=s))

                all = info.popitem()
                data = list(get_detail(s=s, liu=liu, pub_id=pub_id, key=key, pub_info=info))
                if twitter_id == "":
                    id = info["twitter"]
                    if id != "" and id != "Try other keywords":
                        print("no twitter id given. ID retrieved =", id)
                        twitter = gt.main_t(id)
                        # print(twitter)
                        latest_tweet = twitter["tweet"]
                        txt = twitter["txt"]
                        t_info = twitter["info"]
                        twitter_id = id
                        t_all = twitter["all"]
                    elif id == "Try other keywords":
                        print("No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS")
                        latest_tweet = {
                            "tweet_url": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS",
                            "tweet_text": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS",
                            "tweet_date": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS"}
                        txt = ""
                        t_info = {"name": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS",
                                  "about": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS",
                                  "img": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS",
                                  "loc": "No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS"}
                        twitter_id = id
                        t_all = 0

                    else:
                        print("No twitter id given. No twitter retrieved from Linkedin")
                        latest_tweet = {"tweet_url": "", "tweet_text": "", "tweet_date": ""}
                        txt = ""
                        t_info = {"name": "", "about": "", "img": "", "loc": ""}
                        t_all = 0
                else:
                    print("twitter id given. ID =", twitter_id)
                    twitter = gt.main_t(twitter_id)
                    latest_tweet = twitter["tweet"]
                    txt = twitter["txt"]
                    t_info = twitter["info"]
                    t_all = twitter["all"]

            if pub_id == "" and key == "  ":
                print("linkedin handle and keywords not given")
                info = {"linkedin_url": "",
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
                all = []
                data = ["",
                        {"common_IB": {"school_IB": [""],
                                       "skill_IB": [""],
                                       "company_IB": [""],
                                       "location_IB": {"city": "", "state": "", "country": ""}},

                         "uncommon_IB": {"school_IB": [""],
                                         "skill_IB": [""],
                                         "company_IB": [""],
                                         "location_IB": {"city": "", "state": "", "country": ""}}}
                        ]

                if twitter_id == "":
                    print("No twitter id given. No twitter retrieved from Linkedin")
                    latest_tweet = {"tweet_url": "", "tweet_text": "", "tweet_date": ""}
                    txt = ""
                    t_info = {"name": "", "about": "", "img": "", "loc": ""}
                    t_all = 0
                else:
                    print("twitter id given. ID =", twitter_id)
                    twitter = gt.main_t(twitter_id)
                    latest_tweet = twitter["tweet"]
                    txt = twitter["txt"]
                    t_info = twitter["info"]
                    t_all = twitter["all"]

            if clean_name(str(info["first_name"])) == "tryotherkeywords":
                print("FULL NAME NOT FOUND. TRYING FIRST NAME")
                if (len(key_name.split(" ")) > 1):
                    key = str(key_name.split(" ")[:-1][0]) + " " + key_company + " " + key_role
                else:
                    key = key_name + " " + key_company + " " + key_role

                info = dict(e.index(pub_id=pub_id, key=key, s=s))
                all = info.popitem()
                data = list(get_detail(s=s, liu=liu, pub_id=pub_id, key=key, pub_info=info))
                if twitter_id == "":
                    id = info["twitter"]
                    if id != "" and id != "Try other keywords":
                        print("no twitter id given. ID retrieved =", id)
                        twitter = gt.main_t(id)
                        latest_tweet = twitter["tweet"]
                        txt = twitter["txt"]
                        t_info = twitter["info"]
                        twitter_id = id
                        t_all = twitter["all"]
                    elif id == "Try other keywords":
                        print("No twitter id given. No twitter retrieved from Linkedin. TRY OTHER KEYWORDS")
                        latest_tweet = {"tweet_url": "Try other keywords", "tweet_text": "Try other keywords",
                                        "tweet_date": "Try other keywords"}
                        txt = ""
                        t_info = {"name": "Try other keywords", "about": "Try other keywords",
                                  "img": "Try other keywords", "loc": "Try other keywords"}
                        twitter_id = id
                        t_all = 0

                    else:
                        print("No twitter id given. No twitter retrieved from Linkedin")
                        latest_tweet = {"tweet_url": "", "tweet_text": "", "tweet_date": ""}
                        txt = ""
                        t_info = {"name": "", "about": "", "img": "", "loc": ""}
                        t_all = 0
                else:
                    print("twitter id given. ID =", twitter_id)
                    twitter = gt.main_t(twitter_id)
                    latest_tweet = twitter["tweet"]
                    txt = twitter["txt"]
                    t_info = twitter["info"]
                    t_all = twitter["all"]

            ##################################################################################################################################################################
            ##################################################################################################################################################################

            if pub_id != "":
                print("linkedin public handle given")
                tx = {"contact_info_linkedin": info,
                      "contact_info_twitter": {"latest_tweet": latest_tweet,
                                               "contact_info": t_info},
                      "ice_breakers": data[1],
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) == clean_name(
                    str(key_name).lower()):
                print("BOTH SAME")
                tx = {"contact_info_linkedin": info,
                      "contact_info_twitter": {"latest_tweet": latest_tweet,
                                               "contact_info": t_info},
                      "ice_breakers": data[1],
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()) and len(twitter_id) > 0:
                print("BOTH DIFFERENT. USING ONLY TWITTER")
                tx = {"contact_info_linkedin": "LINKEDIN USER -" + str(
                    key_name) + " NOT FOUND. USING ONLY TWITTER",
                      "contact_info_twitter": {"latest_tweet": latest_tweet,
                                               "contact_info": t_info},
                      "ice_breakers": "LINKEDIN USER -" + str(key_name) + " NOT FOUND. USING ONLY TWITTER",
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()) and len(twitter_id) == 0:
                print("BOTH DIFFERENT AND NO TWITTER")
                tx = {"NoLinkedinFoundNoTwitterFound": "Couldn't find any information about -" + str(
                    key_name) + ". Please provide the first name, last name and company name of your contact."}

            elif key == "  " and len(twitter_id) > 0:
                print("ONLY TWITTER GIVEN")
                tx = {"contact_info_linkedin": "USING ONLY TWITTER",
                      "contact_info_twitter": {"latest_tweet": latest_tweet,
                                               "contact_info": t_info},
                      "ice_breakers": "USING ONLY TWITTER",
                      }

            elif pub_id == "" and key == "  " and twitter_id == "":
                print("NOTHING GIVEN")
                tx = {
                    "NoDataGiven": "Please provide atleast the first name, last name and company name of your contact."}

            elif id == "Try other keywords":
                print("TRY OTHER KEYWORDS")
                tx = {"TryOtherKeywords": "Try other keywords"}

        tx["snaphot_retrieval_time"] = int(time.time() - start)
        tx["snapshot_date_time"] = datetime.now()
        tx["snapshot_by"] = req_by
        print(tx)

        if list(tx.keys())[0] == "NoLinkedinFoundNoTwitterFound":
            fin = tx
        else:
            if tx["contact_info_linkedin"] != "" and  tx["ice_breakers"] != "" and \
                    tx["contact_info_twitter"]["latest_tweet"] != "":

                if tx["contact_info_linkedin"] != "LINKEDIN USER -" + str(key_name) + " NOT FOUND. USING ONLY TWITTER" and tx[
                    "contact_info_linkedin"] != "USING ONLY TWITTER":
                    l_han = tx["contact_info_linkedin"]["linkedin_handle"]
                    com_ib = tx["ice_breakers"]["common_IB"]
                    ucom_ib = tx["ice_breakers"]["uncommon_IB"]
                    l_post = tx["contact_info_linkedin"]["latest_linkedin_post"]["post"]
                    l_post_url = tx["contact_info_linkedin"]["latest_linkedin_post"]["url"]
                    l_post_time = tx["contact_info_linkedin"]["latest_linkedin_post"]["time_period"]
                    c_desig = tx["contact_info_linkedin"]["current_company"]["detail"]["title"]
                    c_comp = tx["contact_info_linkedin"]["current_company"]["name"]
                    c_time = tx["contact_info_linkedin"]["current_company"]["detail"]["timePeriod"]


                else:
                    l_han = tx["contact_info_linkedin"]
                    com_ib = tx["ice_breakers"]
                    ucom_ib = tx["ice_breakers"]
                    l_post = tx["contact_info_linkedin"]
                    l_post_url = tx["contact_info_linkedin"]
                    l_post_time = tx["contact_info_linkedin"]
                    c_desig = tx["contact_info_linkedin"]
                    c_comp = tx["contact_info_linkedin"]
                    c_time = tx["contact_info_linkedin"]

                if len(tx["contact_info_twitter"]["contact_info"]["name"]) > 0:
                    t_post = tx["contact_info_twitter"]["latest_tweet"]["tweet_text"]
                    t_post_url = tx["contact_info_twitter"]["latest_tweet"]["tweet_url"]
                    t_post_time = tx["contact_info_twitter"]["latest_tweet"]["tweet_date"]

                else:
                    t_post = ""
                    t_post_url = ""
                    t_post_time = ""

                curr_snap = tx["snapshot_date_time"]
                by = tx["snapshot_by"]
                retr = tx["snaphot_retrieval_time"]

            else:
                l_han = ""
                c_desig = ""
                c_comp = ""
                c_time = ""
                com_ib = ""
                ucom_ib = ""
                l_post = ""
                l_post_url = ""
                l_post_time = ""
                t_post = ""
                t_post_url = ""
                t_post_time = ""
                curr_snap = ""
                by = ""
                retr = ""

            fin = {"LinkedInHandle": l_han, "Contact_Current_Designation": c_desig,
                   "Contact_Current_Company": c_comp, "Current_Company_Since": c_time,
                   "Common_Ice_Breakers": com_ib, "Uncommon_Ice_Breakers": ucom_ib,
                   "latest_linkedin_post": l_post, "latest_linkedin_post_URL": l_post_url,
                   "latest_linkedin_post_time": l_post_time, "latest_tweet": t_post,
                   "latest_tweet_url": t_post_url, "latest_tweet_time": t_post_time,
                   "snapshot_static_date_time": curr_snap, "snapshot_staic_requestedby": by,
                   "snaphot_static_retrieval_time": retr,
                   }

        print(fin)
        return fin