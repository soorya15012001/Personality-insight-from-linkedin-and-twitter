import json

from focal_loss import BinaryFocalLoss
import time
from datetime import datetime
from random import shuffle
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
import requests
from urllib.parse import urlencode
import endpoint_1 as e
import get_twitter as gt
from pymongo import MongoClient

import pickle
import re
from collections import Counter

import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model_middle = SentenceTransformer('bert-base-nli-mean-tokens')


client = MongoClient("mongodb+srv://soorya:soor1234@cluster0.jt4dn.mongodb.net/R_model?retryWrites=true&w=majority")
db = client.get_database("R_model")
r = db.contactIntelligence

nltk.download('stopwords')
nltk.download('wordnet')

headers = {}


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
            if "1 week" not in i["actor"]["subDescription"]["accessibilityText"].lower() and "day" not in i["actor"]["subDescription"]["accessibilityText"].lower() and "hour" not in i["actor"]["subDescription"]["accessibilityText"].lower():
                try:
                    p.append(i["commentary"]["text"]["text"])
                except KeyError:
                    continue
            else:
                continue

        if len(p) == 0:
            p.append("")
            return p
        else:
            if len(p) >15:
                return p[:15]
            else:
                return p
    except:
        return []


def ib_limit(li):
    if len(li) > 3:
        shuffle(li)
        return li[:3]
    elif len(li) <= 3:
        shuffle(li)
        return li


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

    return {"common_IB": {"school_IB": ib_limit([liu_school[i] for i in school_ib]),
                          "skill_IB": ib_limit([liu_skill[i] for i in skill_ib]),
                          "company_IB": ib_limit([liu_comp[i] for i in comp_ib]),
                          "location_IB": {"city": c, "state": s, "country": co}},

            "uncommon_IB": {"school_IB": ib_limit([c_school[i] for i in school_uib]),
                            "skill_IB": ib_limit([c_skill[i] for i in skill_uib]),
                            "company_IB": ib_limit([c_comp[i] for i in comp_uib]),
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
    return padded, s


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
    x = personal + company
    xx = personal + company + post
    # education + article
    x = " ".join(x)
    xx = " ".join(xx)
    return [x, IB, company, post, xx]


# app = Flask(__name__)
# @app.route('/all/', methods=['GET'])
def aa(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token):
    with requests.session() as s:

        # liu = request.args['liu']
        # req_by = request.args['req_by']
        # pub_id = request.args['pub_id']
        # key_name = request.args['key']
        # key_company = request.args['comp']
        # key_role = request.args['role']
        # twitter_id = request.args['twitter_id']

        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = "\"" + csrf_token + "\""
        s.headers["csrf-token"] = csrf_token

        disc_key_traits = {
            "D": "Strong Willed",
            "I": "Open Networker",
            "S": "Likes predictability",
            "C": "Data Driven",

            "DI": "Inspirational",
            "Di": "Assertive and ambitious",
            "DS": "Planners and Results Oriented",
            "Ds": "Planners and Results Oriented",
            "DC": "Entrepreneurial",
            "Dc": "Efficient executors",

            "ID": "Adventurous",
            "Id": "Assertive and charismatic",
            "IS": "Problem Solvers and Adaptive",
            "Is": "Social",
            "IC": "Curious",
            "Ic": "High standards",

            "SD": "Motivated by Challenge",
            "Sd": "Motivated by challenge",
            "SI": "Adaptable and understanding",
            "Si": "Adaptable and understanding",
            "SC": "Cautious and detail oriented",
            "Sc": "Planner",

            "CD": "Executor",
            "Cd": "Problem Solvers",
            "CI": "Conscientious",
            "Ci": "Process Oriented",
            "CS": "Reserved",
            "Cs": "Patient"
        }

        suggestions = {
            "D": {"meetingIntelligence": ["Prepare talking points in advance to get to the point quickly."],
                  "closureIntelligence": ["Summarize key points and avoid emojis.",
                                          "Set responsibilities post meeting."]},

            "I": {
                "meetingIntelligence": ["Get to know them personally.",
                                        "Avoid negative criticism."],
                "closureIntelligence": ["Summarize the big idea."],
            },

            "S": {
                "meetingIntelligence": ["Initiate small talk.",
                                        "Don’t be blunt or too direct.",
                                        "Don’t focus on unproven big ideas."],
                "closureIntelligence": ["Set actionable goals with timelines."],
            },

            "C": {
                "meetingIntelligence": ["Don’t interrupt them."],
                "closureIntelligence": ["Always close the meeting with a detailed email summary with action items."],
            },

            "DI": {
                "meetingIntelligence": ["Speak confidently and ask direct questions.",
                                        "Present high level ideas with direct sentences."],
                "closureIntelligence": ["Summarize with call to action and set definite goals."],
            },

            "Di": {
                "meetingIntelligence": ["Speak confidently.",
                                        "Focus on key points."],
                "closureIntelligence": ["Set actionable next steps with definite goals."],
            },

            "DS": {
                "meetingIntelligence": ["Meet commitments set.",
                                        "Give them time to communicate.",
                                        "Ask questions."],
                "closureIntelligence": ["Don’t rush them.",
                                        "Build trust and relationships."],
            },

            "Ds": {
                "meetingIntelligence": ["Meet commitments set.",
                                        "Give them time to communicate.",
                                        "Ask questions."],
                "closureIntelligence": ["Don’t rush them.",
                                        "Build trust and relationships."],
            },

            "DC": {
                "meetingIntelligence": ["Don't use descriptive phrases.",
                                        "Project your voice confidently and back up everything with a logical reason."],
                "closureIntelligence": ["Close meetings summarize with most important details.",
                                        "Set clear cut roles and deadlines."],
            },

            "Dc": {
                "meetingIntelligence": ["Don't use descriptive phrases.",
                                        "Project your voice confidently and back up everything with a logical reason."],
                "closureIntelligence": ["Close meetings summarize with most important details.",
                                        "Set clear cut roles and deadlines."],
            },

            "ID": {
                "meetingIntelligence": ["Speak positively and recognize their achievements.",
                                        "Meet set commitments."],
                "closureIntelligence": ["Summarize key points and set deadlines"],
            },

            "Id": {
                "meetingIntelligence": ["Speak positively and recognize their achievements.",
                                        "Meet set commitments."],
                "closureIntelligence": ["Summarize key points and set deadlines"],
            },

            "IS": {
                "meetingIntelligence": ["Speak with high energy about new ideas.",
                                        "Interrupt when the discussion tends to go off-track."],
                "closureIntelligence": [
                    "They may not fully commit, so close with a detailed summary with actionable deadlines."],
            },

            "Is": {
                "meetingIntelligence": ["Initiate with small talk.",
                                        "Highlight common connections.",
                                        "Appreciate and respect them."],
                "closureIntelligence": ["Close with win-win proposition."],
            },

            "IC": {
                "meetingIntelligence": ["Don’t confront them.",
                                        "Highlight new ideas."],
                "closureIntelligence": ["Summarize with bullet points.",
                                        "Ask for help."],
            },

            "Ic": {
                "meetingIntelligence": ["Don’t confront them.",
                                        "Highlight new ideas."],
                "closureIntelligence": ["Summarize with bullet points.",
                                        "Ask for help."],
            },

            "SI": {
                "meetingIntelligence": ["Initiate small talk.",
                                        "Appreciate and respect them.",
                                        "Highlight common connections."],
                "closureIntelligence": ["Include additional details.",
                                        "Win as a team."],
            },

            "Si": {
                "meetingIntelligence": ["Initiate small talk.",
                                        "Appreciate and respect them.",
                                        "Highlight common connections."],
                "closureIntelligence": ["Include additional details.",
                                        "Win as a team."],
            },

            "SC": {
                "meetingIntelligence": ["Speak confidently.",
                                        "Share high level ideas.",
                                        "Answer to the point."],
                "closureIntelligence": ["Close meeting with a call to action."],
            },

            "Sc": {
                "meetingIntelligence": ["Speak calmly.",
                                        "Ask questions.",
                                        "Avoid confrontations."],
                "closureIntelligence": ["Summarize actionable items with deadlines.",
                                        "Close with a call to action."],
            },

            "SD": {
                "meetingIntelligence": ["Focus on task at hand.",
                                        "Follow process."],
                "closureIntelligence": ["Summarize with bullet points and avoid emojis.",
                                        "Set actionable goals."],
            },

            "Sd": {
                "meetingIntelligence": ["Focus on task at hand.",
                                        "Follow process."],
                "closureIntelligence": ["Summarize with bullet points.",
                                        "Set actionable goals."],
            },

            "CD": {
                "meetingIntelligence": ["Speak confidently.",
                                        "Avoid metaphors.",
                                        "Back up with logical reasoning."],
                "closureIntelligence": ["Set goals with timelines."],
            },

            "Cd": {
                "meetingIntelligence": ["Highlight new ideas.",
                                        "Get them to focus."],
                "closureIntelligence": ["When closing, set clear goals with deadlines.",
                                        "Set action items for each responsible person."],
            },

            "CI": {
                "meetingIntelligence": ["Be well prepared.",
                                        "Show social proof."],
                "closureIntelligence": ["Summarize with bullet points."],
            },

            "Ci": {
                "meetingIntelligence": ["Be well prepared.",
                                        "Show social proof."],
                "closureIntelligence": ["Summarize with bullet points."],
            },

            "CS": {
                "meetingIntelligence": ["Speak calmly.",
                                        "Ask questions.",
                                        "Explain with details."],
                "closureIntelligence": ["Close formally.",
                                        "Summarize with bullet points."],
            },

            "Cs": {
                "meetingIntelligence": ["Speak calmly.",
                                        "Ask questions.",
                                        "Explain with details."],
                "closureIntelligence": ["Close formally.",
                                        "Summarize with bullet points."],
            }
        }

        disc_suggestions_bin = {
            "D": {"do": ["Clearly state bottom-line and state tasks. Be direct, to the point and brief.",
                         "Focus on “What” instead of “How” e.g. ‘What can this do’ instead of ‘how it does it’.",
                         "When communicating, skip greeting and salutation and get directly to the point of your email. Begin your email with a short subject line, no longer than five words, that states the purpose of the email. They are likely to respond quickly and with one sentence. Don’t be surprised to receive a one-word answer. E.g “Can we set up time on Wednesday to discuss how we can increase your sales prospecting efficiency by 23%?”"],
                  "dont": [
                      "Don’t include other stakeholders unless critical, they prefer to take independent decisions.",
                      "Don't make generalizations or statements without support e.g. Don’t say ‘One of our customer saw great outcome’ instead say ‘Cisco improved Sales prospecting efficiency by 23% in 3 months’."],
                  "Summary": ["They act fast and are motivated by challenges, risks and impact.",
                              "They are risk takers and don’t give up easily.",
                              "They have high expectations from themselves and others."]},

            "I": {"do": [
                "They prefer casual conversation and use a lot of hand gestures and visual aids to get your point across. ",
                "Share the positive impact their decision will have, they are motivated by social recognition.",
                "When communicating, skip greetings but be friendly and try to make a connection. When communicating, greet casually e.g. ‘Hi Sofia’ or ‘Hello Sofia’. Incorporate expressive and friendly language, like an exciting subject line “Enabling a quantum leap in your sales conversions by 23%”. Using punctuation to emphasize your enthusiasm and even an emoji or two will encourage a response more quickly."],
                  "dont": [
                      "Don’t outrightly challenge or reject their ideas, but ask questions. E.g. What do you think of the solution.",
                      "Don’t get impatient or critical even if you disagree with them as they wear their heart on their sleeve."],
                  "Summary": [
                      "They are confident and approachable.",
                      "They deal well with change and respond well to the unexpected, often putting a positive spin on any negative factors.",
                      "They accomplish goals through a sense of humor and influencing people, and use their extroverted, engaging personalities to work any room and win friends.", ]},

            "S": {"do": ["Build a personal rapport and make them feel comfortable.",
                         "Give them time to get started on anything new and be prepared to answer questions e.g. “How does it work?”.",
                         "When communicating, greet formally like “Hello Sofia” and start by introducing yourself. Highlight any possible common connections. Avoid any abbreviations. When closing, always include a call to action for them."],
                  "dont": ["Avoid saying anything that sounds risky and may lead to confrontations.",
                           "Don’t push new ideas, rather show social proof of how it works.",
                           "You won’t get a direct “no” from them, so read between the lines."],
                  "Summary": [
                      "They process information carefully, with intention, and are likely to resent any fast changes or decisions and often take consensus with other stakeholders.",
                      "They might move slowly when there is a big change involved, but they get involved when they are shown long term goals and provided concrete examples of success.",
                      "They focus on planning and preparation to deliver results."]},

            "C": {
                "do": ["Be well prepared and focus on facts and measurable entities.",
                       "Talk about their interests that they can express expertise in rather than engage in personal small talk.",
                       "When communicating, greet formally like “Hello Sofia”. Start by stating the purpose of the email in the subject line. Provide as much information as you can and use a bulleted list to emphasize importance. Make sure you use literal, technically descriptive language and write to them in a steady, somewhat casual tone. Do not use emojis or emphasize your thoughts with lots of punctuation."],
                "dont": ["Don’t break rules or processes with them.",
                         "Do not criticize the work they've already done, as they take great pride in their work.",
                         "Don’t push them for decisions, they take time gathering information and assessing risk before making decisions."],
                "Summary": [
                    "They prefer to work independently and don’t take support from others often, but will play an active part on a team if they can understand how they can add to the overall quality of the outcome.",
                    "They are perfectionistic and have very high standards for both themselves and others.",
                    "They value data and facts over emotions and sometimes may sound harsh when criticizing."]},

            "DI": {
                "do": ["Highlight big picture without going into details.",
                       "Give them authority and ask to give their views.",
                       "When communicating, begin your email with a short subject line, no longer than five words, that states the purpose of the email. If you are interacting for the first time, include a brief and exciting introduction. When closing, always include a call to action for them."],
                "dont": ["Don’t jump between too many features, but focus on one key feature."],
                "Summary": [
                    "They focus on results and end goals in conversation, rather than details or analysis. ",
                    "They are more comfortable with a predictable routine than the unknown but tend to be direct and assertive when it comes to making decisions."]},

            "Di": {
                "do": [
                    "Appeal to their sense of self-worth, they are motivated by achievement, success, and recognition.",
                    "Display strong self-confidence and be a trusted partner or advisor and expect them to have a strong personality.",
                    "When communicating, greet directly with first name e.g. ‘Sofia’ instead of ‘Hi Sofia’ or ‘Hello Sofia’. Take a casual approach and incorporate expressive language, like an exciting subject line “Enabling a quantum leap in your sales conversions by 23%”. Close informally with an ask “Can we set up time on Wednesday to discuss how we can enable a quantum leap in your sales conversions by 23%?” and close with a unique signature e.g. “to new sales”."],
                "dont": ["Don’t be vague and pointless or look like someone who doesn’t know what they are saying.",
                         "Don’t make false commitments, they might get impatient."],
                "Summary": [
                    "They can influence others to support their decisions. They can become your champions, if they believe in your value proposition.",
                    "They are authoritative and like to take charge and can make decisions quickly. They can take risks with logical data.",
                    "They are highly assertive people who, depending on the circumstance, are capable of being amiable and charming or confrontational and direct."]},

            "DS": {"do": ["Showcase low risk, high ROI.",
                          "Win their confidence by doing what you promise and social proof with common contacts."],
                   "dont": ["Don't push them to make a decision early on.",
                            "Don't expect them to take any short-cuts."],
                   "Summary": ["They take pride in their performance and are mostly over achievers.",
                               "They are reliable.",
                               "They are reasonably social and can develop loyalty over time.",
                               "They are very organized, persistent and results are very important to them."]},

            "Ds": {"do": ["Showcase low risk, high ROI.",
                          "Win their confidence by doing what you promise and social proof with common contacts."],
                   "dont": ["Don't push them to make a decision early on.",
                            "Don't expect them to take any short-cuts."],
                   "Summary": ["They take pride in their performance and are mostly over achievers.",
                               "They are reliable.",
                               "They are reasonably social and can develop loyalty over time.",
                               "They are very organized, persistent and results are very important to them."]},

            "DC": {
                "do": ["Show evidence of success.",
                       "Be time conscious and communicate directly, using facts and precise language focusing on the key features with successful outcomes.",
                       "When communicating, greet directly e.g. ‘Sofia’ instead of ‘Hi Sofia’ or ‘Hey Sofia’ and limit your mail to 5 sentences.  Begin your email with a short subject line, no longer than five words, that states the purpose of the email. Mention only the most important details."],
                "dont": ["Don’t be slow in responding back or taking actions.",
                         "Don’t highlight company limitations early on, be confident and positive."],
                "Summary": ["They are focused on results rather than relationships.",
                            "They are not particularly chatty and may actually seem reserved at first.",
                            "Their bluntly assertive style helps them to achieve difficult tasks by sheer force of character.",
                            "They are efficient executors who are concerned with ensuring high standards from themselves and those around them."]},

            "Dc": {
                "do": [
                    "Be time conscious and address issues directly, using facts and precise language focusing on the key features with successful outcomes.",
                    "When communicating, greet directly e.g. ‘Sofia’ instead of ‘Hi Sofia’ or ‘Hey Sofia’ and limit your mail to 5 sentences.  Begin your email with a short subject line, no longer than five words, that states the purpose of the email. Mention only the most important details."],
                "dont": ["Don’t be slow in responding back or taking actions.",
                         "Don’t highlight company limitations early on, be confident and positive."],
                "Summary": ["They are more focused on results than relationships.",
                            "They are efficient executors who are concerned with ensuring high standards from themselves and those around them.",
                            "They can’t be won over easily. They rely on evidence of success and can make fast decisions."]},

            "ID": {
                "do": [
                    "Engage with stories and appeal to their sense of self-worth, they are motivated by achievement, success, and recognition.",
                    "Focus on one problem at a time.",
                    "When communicating, greet directly e.g. ‘Sofia’ instead of ‘Hi Sofia’ or ‘Hey Sofia’. Define the purpose of an email in the first sentence. Take a casual approach and incorporate expressive language."],
                "dont": ["Don’t make fake promises.",
                         "Don’t hesitate from asking questions and pushing them."],
                "Summary": [
                    "They are highly assertive people who, depending on the circumstance, are capable of being direct and dynamic or charming and amiable.",
                    "They welcome challenging projects. They look for the big picture and can create new opportunities.",
                    "They don’t like to follow processes or routines."]},

            "Id": {
                "do": [
                    "Engage with stories and appeal to their sense of self-worth, they are motivated by achievement, success, and recognition.",
                    "Focus on one problem at a time.",
                    "When communicating, greet directly e.g. ‘Sofia’ instead of ‘Hi Sofia’ or ‘Hey Sofia’. Define the purpose of an email in the first sentence. Take a casual approach and incorporate expressive language."],
                "dont": ["Don’t make fake promises.",
                         "Don’t hesitate from asking questions and pushing them."],
                "Summary": [
                    "They are highly assertive people who, depending on the circumstance, are capable of being direct and dynamic or charming and amiable.",
                    "They welcome challenging projects. They look for the big picture and can create new opportunities.",
                    "They don’t like to follow processes or routines."]},

            "IS": {"do": [
                "Highlight any mutual connections or common workplace upfront. They open up more if you are friendly, amiable and have something in common.",
                "If possible get introduced through a common connection. Highlight common connections upfront and showcase your strength on how they are using your product.",
                "When communicating, use informal greetings (e.g. ‘Hey Sofia’ instead of  ‘Hello Sofia’) and use expressive language with detailed mail and bullet points and add any attachments or additional data."],
                   "dont": ["Don’t push them for making decisions, assume the deal will move slowly.",
                            "Don’t highlight the risks of your product upfront."],
                   "Summary": ["They value relationships and prefer detailed conversations compared to small talk.",
                               "They usually consult others before making a big decision.",
                               "They are excited by new ideas and usually very open to new people."
                               "Win-win situations work well with them."]},

            "Is": {"do": ["Involve people close to them for decision making and idea sharing.",
                          "Speak with welcoming tone and highlight your strengths with social proof.",
                          "When communicating, use informal greetings (e.g. ‘Hey Sofia’ instead of  ‘Hello Sofia’) and use expressive language with detailed mail and bullet points and add any attachments or additional data."],
                   "dont": ["Don't take unproved risks.",
                            "Don’t push them for making decisions or make them uncomfortable."],
                   "Summary": ["They believe in proven solutions.",
                               "They are people oriented and do well with teams. They excel at collaboration and value relationships over results.",
                               "They can easily differentiate between the big picture and non-obvious goals.",
                               "Win-win situations work well with them."]},

            "IC": {
                "do": ["Show them in good light in front of others.",
                       "Build a trusting environment for them to open up.",
                       "Be clear of your expectations from them"],
                "dont": ["Don't pressurize", "Don’t expect detailed feedback."],
                "Summary": ["They are highly competitive and imaginative at the same time.",
                            "They have the skills to bring unique solutions.",
                            "They sometimes get overworked and exhausted with their own analysis and solutions.",
                            "They appear confident and extroverts with friends but may tend to be more cautious in the business world, so they might seem unpredictable."]},

            "Ic": {
                "do": ["Show them in good light in front of others.",
                       "Build a trusting environment for them to open up.",
                       "Be clear of your expectations from them"],
                "dont": ["Don't pressurize", "Don’t expect detailed feedback."],
                "Summary": ["They are highly competitive and imaginative at the same time.",
                            "They have the skills to bring unique solutions.",
                            "They sometimes get overworked and exhausted with their own analysis and solutions.",
                            "They appear confident and extroverts with friends but may tend to be more cautious in the business world, so they might seem unpredictable."]},

            "SI": {
                "do": [
                    "Be friendly and amiable and highlight teamwork and be open to include others in decision making process.",
                    "Be open to cancellations or sudden changes.",
                    "When communicating, use casual greeting (e.g. Hey Sofia’ instead of Hi Sofia’) and express yourself with details."],
                "dont": ["Don’t push them for making decisions or make them uncomfortable.",
                         "Don’t focus on unproven features."],
                "Summary": ["They are very social.",
                            "They are understanding and help others in achieving their goals.",
                            "They adapt to difficult situations easily and try to reduce conflict with others.",
                            "They are warm and confident and are always ready to help with another's problems."]},

            "Si": {
                "do": [
                    "Be friendly and amiable and highlight teamwork and be open to include others in decision making process.",
                    "Be open to cancellations or sudden changes.",
                    "When communicating, use casual greeting (e.g. Hey Sofia’ instead of Hi Sofia’) and express yourself with details."],
                "dont": ["Don’t push them for making decisions or make them uncomfortable.",
                         "Don’t focus on unproven features."],
                "Summary": ["They are very social.",
                            "They are understanding and help others in achieving their goals.",
                            "They adapt to difficult situations easily and try to reduce conflict with others.",
                            "They are warm and confident and are always ready to help with another's problems."]},

            "SC": {"do": ["Present solutions at high level without going into details.",
                          "Expect clarity seeking questions e.g. “How does this work?”, answer with authority and calmness.",
                          "When communicating, don’t use greetings or salutations, greet with a first name like “Sofia”. State your purpose in the first sentence of your email. Limit email to 5 sentences or less. Highlight any possible common connections. Always close with a call to action."],
                   "dont": ["Don’t get into storytelling mode, especially when they ask pointed questions.",
                            "Avoid pushing them for a quick decision, they take time with high-risk decisions."],
                   "Summary": [
                       "They are usually reserved and prefer to build trust with a small group of close friends rather than a large one.",
                       "Sometimes, they may be considered as low risk takers, but place high value on results, stability, and fairness. They are more comfortable with a predictable routine than the unknown.",
                       "They provide support and guidance and make others feel at ease."]},

            "Sc": {"do": ["Ask questions and pause occasionally to invite them to speak.",
                          "They expect accuracy in everything, so provide additional details or information."
                          "Keep some margin because they like to negotiate.",
                          "When communicating, greet formally like “Hello Sofia” and start by introducing yourself. Highlight any possible common connections. Use bullet points in your email rather than long paragraphs. Add links to additional reference documents. Avoid abbreviations and emojis. Close formally and always include a call to action for them."],
                   "dont": ["Don’t give superficial answers and avoid highlighting uncertainties.",
                            "You won’t get a direct ‘no’ from them, so read between the lines.",
                            "Avoid emotionally charged situations with them."],
                   "Summary": [
                       "In most situations they will go for low-risk and proven solutions. Way to win over them is to show proof of success.",
                       "They are motivated by predictability, loyalty and security.",
                       "They are perfectionists and very thoughtful in their approach. They rely on logic and analysis but are accommodating. ",
                       "They plan in advance and expect others to be prepared too."]},

            "SD": {
                "do": ["Focus on impact, stability and certainty.",
                       "Involve other key stakeholders in decision making.",
                       "When communicating, skip greeting and salutation and get directly to the point of your email. Begin your email with a short subject line, no longer than five words, that states the purpose of the email. Close with a formal ask E.g “If you are available on Wednesday, shall I send you a meeting request to discuss further?”"],
                "dont": ["Don’t tell the big picture at once but focus on one thing that needs to get done.",
                         "Don't force them into decision making."],
                "Summary": ["They are task oriented and like to get things done in a friendly but thorough manner.",
                            "They are both energetic and stable and sometimes can be very persistent.",
                            "They are patient with others and will stick with a task until it’s done."]},

            "Sd": {
                "do": ["Focus on impact, stability and certainty.",
                       "Involve other key stakeholders in decision making.",
                       "When communicating, skip greeting and salutation and get directly to the point of your email. Begin your email with a short subject line, no longer than five words, that states the purpose of the email. Close with a formal ask E.g “If you are available on Wednesday, shall I send you a meeting request to discuss further?”"],
                "dont": ["Don’t tell the big picture at once but focus on one thing that needs to get done.",
                         "Don't force them into decision making."],
                "Summary": ["They are task oriented and like to get things done in a friendly but thorough manner.",
                            "They are both energetic and stable and sometimes can be very persistent.",
                            "They are patient with others and will stick with a task until it’s done."]},

            "CD": {
                "do": ["Speak clearly and confidently and backup your claims with data.",
                       "Provide them with relevant data to help them make a decision.",
                       "When communicating, use direct greetings like “Sofia” instead of “Hello Sofia” and be very professional. State the purpose of the email in the first sentence, and limit your email to 3 sentences or less. Focus only on the most important details. They are likely to respond with one sentence. Don’t be surprised to receive a one-word answer."],
                "dont": ["Don’t make them feel that they are losing control.",
                         "Don’t be rattled if they go against you or show disinterest or become critical."],
                "Summary": [
                    "They are incredibly detailed and result oriented. They have high standards and expect others to meet their expectations.",
                    "They are great executors and like to be in control.",
                    "They move fast and get impatient when things get blocked or standards not met."]},

            "Cd": {
                "do": [
                    "Speak quickly with high energy about new ideas and abstract philosophy instead of engaging in small talk.",
                    "When communicating, use informal greetings like “Hey Sofia” instead of “Hello Sofia”. Use friendly, expressive language to describe feelings and ideas. Include all relevant information and attachments. Use bulleted lists and external data."],
                "dont": ["Don’t make them feel that they are losing control.",
                         "Don’t focus on process or routine.",
                         "Don’t make bold claims without supporting documents."],
                "Summary": ["They are problem solvers with a big appetite for change and dislike routine.",
                            "They love new ideas and are good networkers and if asked, can help make new connections.",
                            "They tend to make decisions based on logic rather than emotions.",
                            "They place high value on efficiency, accuracy, and logic."]},

            "CI": {"do": ["They are well researched, so approach them with data and proof.",
                          "Articulate well and show Results."],
                   "dont": ["Don’t put them under pressure as they get exhausted and irritated.",
                            "Don't be judgemental of the work they have done."],
                   "Summary": [
                       "They appear confident and extroverts with friends but may tend to be more cautious in the business world.",
                       "Praise them on their achievements.",
                       "They are a unique blend of creative and critical."]},

            "Ci": {"do": ["They are well researched, so approach them with data and proof.",
                          "Articulate well and show Results."],
                   "dont": ["Don’t put them under pressure.",
                            "Don't be judgemental of the work they have done."],
                   "Summary": [
                       "They are imaginative and creative.",
                       "They prefer to work in groups of known people.",
                       "They might be shy when meeting for the first time and not open to share personal information.",
                       "When communicating be warm and friendly and create trust."]},

            "CS": {"do": ["Speak in calm and steady voice and focus on facts and measurable entities.",
                          "Ask lots of questions and pause occasionally to invite them to speak.",
                          "When communicating, use formal greetings (e.g. ‘Hi Sofia’ or ‘Hello Sofia’ instead of ‘Hey Sofia’). Use bullet points instead of long paragraphs. Avoid abbreviations or emojis. Provide additional details via attachments or external links."],
                   "dont": ["Don’t make false promises.",
                            "Don’t surprise them, tell them what to expect beforehand."],
                   "Summary": ["They are often perfectionists and expect the same from others.",
                               "They rely on data to make decisions and separate emotions from decision making.",
                               "They are usually happy to take a supporting role, but influence decisions.",
                               "They might be hesitant to try new solutions, often going ahead with proven solutions."]},

            "Cs": {"do": ["Speak in calm and steady voice and focus on facts and measurable entities.",
                          "Ask lots of questions and pause occasionally to invite them to speak.",
                          "When communicating, use formal greetings (e.g. ‘Hi Sofia’ or ‘Hello Sofia’ instead of ‘Hey Sofia’). Use bullet points instead of long paragraphs. Avoid abbreviations or emojis. Provide additional details via attachments or external links."],
                   "dont": ["Don’t make false promises.",
                            "Don’t surprise them, tell them what to expect beforehand."],
                   "Summary": ["They are often perfectionists and expect the same from others.",
                               "They rely on data to make decisions and separate emotions from decision making.",
                               "They are usually happy to take a supporting role, but influence decisions.",
                               "They might be hesitant to try new solutions, often going ahead with proven solutions."]}
        }

        mbti_traits = {
            "ISTJ": ["Reliable",
                     "Organized",
                     "Practical"],

            "ISTP": ["Curious and adventurous",
                     "Self confident",
                     "Pragmatic"],

            "ISFJ": ["Loyal",
                     "Practical",
                     "Perfectionists"],

            "ISFP": ["Practical",
                     "Curious",
                     "Imaginative and Artistic"],

            "INFJ": ["Perfectionists",
                     "Reserved",
                     "Highly creative and artistic"],

            "INFP": ["Reserved",
                     "Idealistic",
                     "Empathetic"],

            "INTJ": ["Independent",
                     "Curious and Original",
                     "Ambitious"],

            "INTP": ["Big Picture",
                     "Abstract thinker",
                     "Objective"],

            "ESTP": ["Influential & persuasive",
                     "Logical",
                     "Action-oriented"],

            "ESTJ": ["Practical",
                     "Dependable",
                     "Hard working"],

            "ESFP": ["Optimistic",
                     "Networker",
                     "Supportive"],

            "ESFJ": ["Dependable",
                     "Organized",
                     "Strong sense of Duty"],

            "ENFP": ["Enthusiastic",
                     "Adaptable",
                     "Inventive"],

            "ENFJ": ["Empathetic",
                     "Protagonist",
                     "Altruistic"],

            "ENTP": ["Innovative",
                     "Expressive",
                     "Great conversationalist"],

            "ENTJ": ["Results Oriented",
                     "Decision Maker",
                     "Charismatic and Inspiring"]}

        mbti_suggestions = {
            "ISTJ": {"do": ["Focus on details and logic rather than the big picture.",
                            "They follow structure and rules and highly appreciate integrity and honesty."],
                     "dont": ["Don't make them take last-minute adjustments.",
                              "Be honest and direct, don’t beat around the bush."],
                     "summary": [
                         "They are planners; they like to carefully plan things out well in advance and strive hard to meet their commitments.",
                         "They compose their actions carefully and carry them out with methodical purpose."]},

            "ISFJ": {
                "do": ["They are good at remembering details about other people. Be careful when committing anything."],
                "dont": [
                    "Don’t give abstract or hypothetical situations, but specific details e.g. “We helped Amazon get 20% more prospecting summary to help them increase their topline by 2%”.",
                    "Don’t criticize openly. When they encounter criticism or disagreement, even if it’s well intentioned, they may feel as if they’re experiencing a personal attack."],
                "summary": ["They can be meticulous to the point of perfectionism.",
                            "They struggle with change. "]},

            "ESTJ": {
                "do": [
                    "They are very organized and follow rules. Send meeting invites well in advance, set the agenda and end with a summary of most important details.",
                    "They take pride in the respect of their friends, colleagues and community and while difficult to admit, are very concerned with public opinion."],
                "dont": ["They value dependability, don’t miss your commitments.",
                         "Don’t cut corners or compromise on rules and processes."],
                "summary": ["They are very principled and lead by example.",
                            "They are efficient executors who are concerned with ensuring high standards from themselves and those around them. They can at times appear critical and overly aggressive, particularly when other people fail to live up to their high standards."]},

            "ESFJ": {"do": ["Make them feel appreciated and build long term trust and relationships."],
                     "dont": ["Don’t give negative feedback openly, they get hurt by unkindness or indifference."],
                     "summary": [
                         "Their achievements are guided by decisive values, and they willingly and sincerely offer guidance and help to others.",
                         "They sometimes tend to make decisions based on their emotions and concern for others."]},

            "ISTP": {"do": ["Tell them 'what', not 'how’."],
                     "dont": ["Don't micromanage them or do multiple follow-ups.",
                              "They don’t like commitments."],
                     "summary": [
                         "They tend to focus on details and logic but are more interested in practical applications than in abstract ideas.",
                         "They are good at keeping a cool head, maintaining their objectivity, and coping with crisis."]},

            "ISFP": {"do": ["Show them how things work.", "Set clear goals with deadlines."],
                     "dont": [
                         "Don’t bind them into rules and regulations, they are spontaneous and prefer the unexpected.",
                         "Don’t push them for decisions, but keep them engaged. They like to keep their options open, so they often delay making decisions in order to see if things might change or if new options come up."],
                     "summary": ["They tend to challenge rules.",
                                 "They like to focus on the details. They spend more time thinking about the here and now rather than worrying about the future."]},

            "ESTP": {"do": [
                "Be careful when sharing details, they are very observant, often picking up on details that other people never notice."],
                     "dont": ["Don’t write elaborate emails, but get to the point."],
                     "summary": [
                         "They tend to make quick decisions. When confronted by problems, they quickly look at the facts and devise an immediate solution. They tend to improvise rather than spend a great deal of time planning.",
                         "They don't have a lot of use for abstract theories or concepts. They are more practical, preferring straightforward information that they can think about rationally and act upon immediately."]},

            "ESFP": {
                "do": ["Engage in small-talk, build relationships and stay in constant touch."],
                "dont": ["Don't be publicly critical. They are strongly emotional, and very vulnerable to criticism."],
                "summary": ["They are observant and have a keen eye for any changes.",
                            "They can be very social, often encouraging others into shared activities."]},

            "INFJ": {"do": [
                "Share the big picture and complexity, they are energized and impassioned by the beauty of their visions for the future."],
                     "dont": [
                         "Don’t criticize openly. They may be sensitive to criticism, when it comes to the issues that are near and dear to them, they can become defensive or dismissive."],
                     "summary": [
                         "They are idealists and principled with unwavering commitment, they aren’t content to coast through life – they want to stand up and make a difference.",
                         "They are perfectionists. Both logical and emotional, creative and analytical."]},

            "INFP": {"do": [
                "Give them space to think on solutions to complex problems. They often delay making important decisions just in case something about the situation changes."],
                     "dont": ["Don’t give blunt or critical feedback openly, they may take it personally."],
                     "summary": ["They tend to be quiet, open-minded, imaginative.",
                                 "They rely on intuition and are more focused on the big picture rather than the nitty-gritty details."]},

            "ENFP": {"do": ["Meet commitments.", "Highlight if there are any common connections."],
                     "dont": ["Avoid structure and routine with them.", "Don’t focus too much on details."],
                     "summary": [
                         "They are true free spirits – outgoing, openhearted, and open-minded. With their lively, upbeat approach to life, they stand out in any crowd.",
                         "They are creative and do best in situations where they have the freedom to be creative and innovative."]},

            "ENFJ": {"do": ["Do show that you accept and appreciate what they have to offer."],
                     "dont": ["Don’t give harsh criticism, they might take it personally."],
                     "summary": [
                         "They love helping others. When they care about someone, they want to help solve that person’s problems – sometimes at any cost.",
                         "They tend to be vocal about their values, including authenticity and altruism. When something strikes them as unjust or wrong, they speak up."]},

            "INTJ": {"do": [
                "Be careful in your communication, they are good at 'reading between the lines' to figure out what things might really mean."],
                     "dont": ["Avoid lengthy emails, be direct, clear and precise."],
                     "summary": [
                         "Focus on the big picture and on abstract information rather than concrete details, they enjoy thinking about the future and exploring possibilities."]},

            "INTP": {"do": ["They are quick to detect factual inconsistencies, and be careful when sharing details."],
                     "dont": ["Don’t get emotional, they may appear insensitive sometimes."],
                     "summary": [
                         "They love discovering new theories and ideas in their field. They spend more time perfecting rather than getting to a workable solution.",
                         "They are logical and base decisions on objective information rather than subjective feelings."]},

            "ENTP": {"do": [
                "They are often willing to play the devil's advocate, they enjoy debates as a way of exploring a topic, learning what other people believe, and helping others see the other side of the story. To gain their attention, use wit and highlight originality."],
                     "dont": [
                         "Don’t push them for outcomes. Instead of making a decision or committing to a course of action, they would prefer to wait and see what happens."],
                     "summary": ["They pursue their goals vigorously despite any resistance they might encounter.",
                                 "They are more focused on the future rather than on immediate details."]},

            "ENTJ": {"do": ["Present a big vision, set measurable goals and meet deadlines/ commitments.",
                            "Objective, rational statements about what is done right and what can be done better are helpful to, they appreciate them."],
                     "dont": ["Avoid stagnancy and getting emotional."],
                     "summary": [
                         "They aim for big goals and push their goals through with sheer willpower where others might give up and move on.",
                         "They are decisive people who love momentum and accomplishment."]}
        }

        start = time.time()

        key = key_name + " " + key_company + " " + key_role
        text_fin = ""
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
            # [x, ib, company, post]

            if pub_id != "":
                print("linkedin public handle given")

                if len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) > 75:
                    dd = str(data[0])
                    x, text_fin = clean(str(data[0]))

                elif len("".join(data[3]).split()) + len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) > 75:
                    dd = str(data[-1])
                    x, text_fin = clean(str(data[-1]))

                elif len("".join(data[3]).split()) + len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) + len(str(txt).split()) > 50:
                    dd = str(data[-1]) + " " + str(txt)
                    x, text_fin = clean(str(data[-1]) + str(txt))

                else:
                    dd = ""
                    x, text_fin = "", ""

                if len(dd) != 0:

                    f = open('middle_ware_data_separate.json')
                    data_mid = json.load(f)
                    # data_mid = pd.read_csv("middle_ware_data_separate.json")

                    chosen_model = data_mid["model"]
                    loaded_mid = np.load('embedding_separate.npz')['arr_0']
                    text_mid = [text_fin]
                    ip = model_middle.encode(text_mid)
                    cos = cosine_similarity(ip, loaded_mid)
                    t = {}
                    for i, j in zip(cos[0], chosen_model):
                        t[i] = j
                    print(t[max(t.keys())])
                    print(max(t.keys()))
                    if t[max(t.keys())] == 1:
                        print("############### CNN_CE_B_SM")
                        model_l = load_model("models/cnn_CE_B_SM.h5")
                        label_J = load_model("models/cnn_MBTI_CE_B_SM.h5")
                    else:
                        print("############### CNN_FL_UB")
                        model_l = load_model("models/cnn_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})
                        label_J = load_model("models/cnn_MBTI_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})

                    disc = ["D", "I", "S", "C"]
                    mbti = ['ESFJ', 'ESFP', 'ISFJ', 'ISFP', 'INTJ', 'ENFP', 'ENFJ', 'ISTP', 'INFJ', 'ESTP', 'ESTJ',
                            'ENTJ', 'INTP', 'INFP', 'ISTJ', 'ENTP']

                    z = {}
                    zz = {}

                    for i, j in zip(disc, model_l.predict(x).tolist()[0]):
                        z[i] = j

                    for i, j in zip(mbti, label_J.predict(x).tolist()[0]):
                        zz[i] = j
                    z = sorted(z.items(), key=lambda d: d[1], reverse=True)
                    com = round(abs(z[0][1] - z[1][1]), 2)
                    print(com)

                    zz = sorted(zz.items(), key=lambda d: d[1], reverse=True)

                    if (com < 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]))]]
                        shuffle(eng)

                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0])))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }


                    elif (com < 0.8 and com >= 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]).lower())]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0]).lower()))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }
                    else:
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0])]]
                        do = list(disc_suggestions_bin[str(z[0][0])]["do"]) + mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0])]["dont"]) + mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0])]["Summary"]) + mbti_suggestions[str(zz[0][0])][
                            "summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(z[0][0])},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1])
                              }
                else:
                    tx = {"NoTextExtractedError": "User found but not enough text - " + info[
                        "linkedin_handle"] + ", Headline " + str(len(info["headline"].split())) + " , about " + str(
                        len(info["about"].split())) + " , job desc " + str(
                        len("".join(data[2]).split())) + " , posts " + str(len("".join(data[3]).split()))}

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) == clean_name(
                    str(key_name).lower()):
                print("BOTH SAME")

                if len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) > 75:
                    dd = str(data[0])
                    x, text_fin = clean(str(data[0]))

                elif len("".join(data[3]).split()) + len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) > 75:
                    dd = str(data[-1])
                    x, text_fin = clean(str(data[-1]))

                elif len("".join(data[3]).split()) + len(info["about"].split() + info["headline"].split() + "".join(data[2]).split()) + len(str(txt).split()) > 50:
                    dd = str(data[-1]) + " " + str(txt)
                    x, text_fin = clean(str(data[-1]) + " " + str(txt))

                print(x, text_fin)

                if len(dd) != 0:

                    f = open('middle_ware_data_separate.json')
                    data_mid = json.load(f)
                    # data_mid = pd.read_csv("middle_ware_data_separate.json")

                    chosen_model = data_mid["model"]
                    loaded_mid = np.load('embedding_separate.npz')['arr_0']
                    text_mid = [text_fin]
                    ip = model_middle.encode(text_mid)
                    cos = cosine_similarity(ip, loaded_mid)
                    t = {}
                    for i, j in zip(cos[0], chosen_model):
                        t[i] = j

                    if t[max(t.keys())] == 1:
                        print("############### CNN_CE_B_SM")
                        model_l = load_model("models/cnn_CE_B_SM.h5")
                        label_J = load_model("models/cnn_MBTI_CE_B_SM.h5")
                    else:
                        print("############### CNN_FL_UB")
                        model_l = load_model("models/cnn_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})
                        label_J = load_model("models/cnn_MBTI_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})

                    disc = ["D", "I", "S", "C"]
                    mbti = ['ESFJ', 'ESFP', 'ISFJ', 'ISFP', 'INTJ', 'ENFP', 'ENFJ', 'ISTP', 'INFJ', 'ESTP', 'ESTJ',
                            'ENTJ', 'INTP', 'INFP', 'ISTJ', 'ENTP']

                    z = {}
                    zz = {}

                    for i, j in zip(disc, model_l.predict(x).tolist()[0]):
                        z[i] = j

                    for i, j in zip(mbti, label_J.predict(x).tolist()[0]):
                        zz[i] = j
                    z = sorted(z.items(), key=lambda d: d[1], reverse=True)
                    com = round(abs(z[0][1] - z[1][1]), 2)
                    print(com)

                    zz = sorted(zz.items(), key=lambda d: d[1], reverse=True)

                    if (com < 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]))]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0])))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }


                    elif (com < 0.8 and com >= 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]).lower())]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0]).lower()))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }
                    else:
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0])]]
                        do = list(disc_suggestions_bin[str(z[0][0])]["do"]) + mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0])]["dont"]) + mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0])]["Summary"]) + mbti_suggestions[str(zz[0][0])][
                            "summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": info,
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": data[1],

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(z[0][0])},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1])
                              }

                else:
                    tx = {"NoTextExtractedError": "User found but not enough text - " + info[
                        "linkedin_handle"] + ", Headline " + str(len(info["headline"].split())) + " , about " + str(
                        len(info["headline"].split())) + " , job desc " + str(
                        len("".join(data[2]).split())) + " , posts " + str(len("".join(data[3]).split()))}

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()) and len(
                twitter_id) > 0 and twitter_id != "Try other keywords" and pub_id != "Try other keywords":
                print("BOTH DIFFERENT. USING ONLY TWITTER")
                dd = str(txt)
                x, text_fin = clean(str(txt))

                if len(dd) != 0:

                    f = open('middle_ware_data_separate.json')
                    data_mid = json.load(f)
                    # data_mid = pd.read_csv("middle_ware_data_separate.json")

                    chosen_model = data_mid["model"]
                    loaded_mid = np.load('embedding_separate.npz')['arr_0']
                    text_mid = [text_fin]
                    ip = model_middle.encode(text_mid)
                    cos = cosine_similarity(ip, loaded_mid)
                    t = {}
                    for i, j in zip(cos[0], chosen_model):
                        t[i] = j

                    if t[max(t.keys())] == 1:
                        print("############### CNN_CE_B_SM")
                        model_l = load_model("models/cnn_CE_B_SM.h5")
                        label_J = load_model("models/cnn_MBTI_CE_B_SM.h5")
                    else:
                        print("############### CNN_FL_UB")
                        model_l = load_model("models/cnn_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})
                        label_J = load_model("models/cnn_MBTI_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})

                    disc = ["D", "I", "S", "C"]
                    mbti = ['ESFJ', 'ESFP', 'ISFJ', 'ISFP', 'INTJ', 'ENFP', 'ENFJ', 'ISTP', 'INFJ', 'ESTP', 'ESTJ',
                            'ENTJ', 'INTP', 'INFP', 'ISTJ', 'ENTP']

                    z = {}
                    zz = {}

                    for i, j in zip(disc, model_l.predict(x).tolist()[0]):
                        z[i] = j

                    for i, j in zip(mbti, label_J.predict(x).tolist()[0]):
                        zz[i] = j
                    z = sorted(z.items(), key=lambda d: d[1], reverse=True)
                    com = round(abs(z[0][1] - z[1][1]), 2)
                    print(com)

                    zz = sorted(zz.items(), key=lambda d: d[1], reverse=True)


                    if (com < 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]))]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "LINKEDIN USER -" + str(
                            key_name) + " NOT FOUND. USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "LINKEDIN USER -" + str(key_name) + " NOT FOUND. USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0])))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }


                    elif (com < 0.8 and com >= 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]).lower())]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "LINKEDIN USER -" + str(
                            key_name) + " NOT FOUND. USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "LINKEDIN USER -" + str(key_name) + " NOT FOUND. USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0]).lower()))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }
                    else:
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0])]]
                        do = list(disc_suggestions_bin[str(z[0][0])]["do"]) + mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0])]["dont"]) + mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0])]["Summary"]) + mbti_suggestions[str(zz[0][0])][
                            "summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "LINKEDIN USER -" + str(
                            key_name) + " NOT FOUND. USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "LINKEDIN USER -" + str(key_name) + " NOT FOUND. USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(z[0][0])},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1])
                              }
                else:
                    tx = {"NoTextExtractedError": "User found but not enough text - " + info[
                        "linkedin_handle"] + ", Headline " + str(len(info["headline"].split())) + " , about " + str(
                        len(info["headline"].split())) + " , job desc " + str(
                        len("".join(data[2]).split())) + " , posts " + str(len("".join(data[3]).split()))}

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()) and len(
                twitter_id) == 0 and twitter_id == "Try other keywords" and pub_id == "Try other keywords":
                print("BOTH DIFFERENT AND NO TWITTER")
                tx = {"NoLinkedinFoundNoTwitterFound": "Couldn't find any information about -" + str(
                    key_name) + ". Please provide the first name, last name and company name of your contact."}

            elif key == "  " and len(twitter_id) > 0:
                print("ONLY TWITTER GIVEN")
                dd = str(txt)
                x, text_fin = clean(str(txt))

                if len(dd) != 0:

                    f = open('middle_ware_data_separate.json')
                    data_mid = json.load(f)
                    # data_mid = pd.read_csv("middle_ware_data_separate.json")

                    chosen_model = data_mid["model"]
                    loaded_mid = np.load('embedding_separate.npz')['arr_0']
                    text_mid = [text_fin]
                    ip = model_middle.encode(text_mid)
                    cos = cosine_similarity(ip, loaded_mid)
                    t = {}
                    for i, j in zip(cos[0], chosen_model):
                        t[i] = j

                    if t[max(t.keys())] == 1:
                        print("############### CNN_CE_B_SM")
                        model_l = load_model("models/cnn_CE_B_SM.h5")
                        label_J = load_model("models/cnn_MBTI_CE_B_SM.h5")
                    else:
                        print("############### CNN_FL_UB")
                        model_l = load_model("models/cnn_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})
                        label_J = load_model("models/cnn_MBTI_FL_UB.h5", custom_objects={'loss': BinaryFocalLoss})

                    disc = ["D", "I", "S", "C"]
                    mbti = ['ESFJ', 'ESFP', 'ISFJ', 'ISFP', 'INTJ', 'ENFP', 'ENFJ', 'ISTP', 'INFJ', 'ESTP', 'ESTJ',
                            'ENTJ', 'INTP', 'INFP', 'ISTJ', 'ENTP']

                    z = {}
                    zz = {}

                    for i, j in zip(disc, model_l.predict(x).tolist()[0]):
                        z[i] = j

                    for i, j in zip(mbti, label_J.predict(x).tolist()[0]):
                        zz[i] = j
                    z = sorted(z.items(), key=lambda d: d[1], reverse=True)
                    com = round(abs(z[0][1] - z[1][1]), 2)
                    print(com)

                    zz = sorted(zz.items(), key=lambda d: d[1], reverse=True)

                    if (com < 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]))]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]))]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0])))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }


                    elif (com < 0.8 and com >= 0.5):
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0] + str(z[1][0]).lower())]]
                        do = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["do"]) + \
                             mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["dont"]) + \
                               mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0] + str(z[1][0]).lower())]["Summary"]) + \
                                  mbti_suggestions[str(zz[0][0])]["summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(str(z[0][0] + str(z[1][0]).lower()))},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1]) / 2 + float(z[1][1]) / 2
                              }
                    else:
                        eng = list(mbti_traits[str(zz[0][0])])
                        shuffle(eng)

                        eng = eng + [disc_key_traits[str(z[0][0])]]
                        do = list(disc_suggestions_bin[str(z[0][0])]["do"]) + mbti_suggestions[str(zz[0][0])]["do"]
                        dont = list(disc_suggestions_bin[str(z[0][0])]["dont"]) + mbti_suggestions[str(zz[0][0])]["dont"]
                        summary = list(disc_suggestions_bin[str(z[0][0])]["Summary"]) + mbti_suggestions[str(zz[0][0])][
                            "summary"]
                        meet = suggestions[str(z[0][0] + str(z[1][0]))]["meetingIntelligence"]
                        close = suggestions[str(z[0][0] + str(z[1][0]))]["closureIntelligence"]

                        shuffle(do)
                        shuffle(dont)
                        shuffle(summary)
                        shuffle(meet)
                        shuffle(close)

                        tx = {"contact_info_linkedin": "USING ONLY TWITTER",
                              "contact_info_twitter": {"latest_tweet": latest_tweet,
                                                       "contact_info": t_info},
                              "ice_breakers": "USING ONLY TWITTER",

                              "meet_close": {"meetingIntelligence": meet, "closureIntelligence": close},
                              "EngIntel": eng,
                              "do": do,
                              "dont": dont,
                              "summary": summary,

                              "disc_info": {"disc": str(z[0][0])},
                              "mbti_info": {"mbti": str(zz[0][0])},
                              "accuracy": float(z[0][1])
                              }
                else:
                    tx = {
                        "NoTweetExtractedError": "Twitter handle " + str(
                            twitter_id) + " not found. Please try again or use a different handle"}

            elif pub_id == "" and key == "  " and twitter_id == "":
                print("NOTHING GIVEN")
                tx = {
                    "NoDataGiven": "Please provide atleast the first name, last name and company name of your contact."}

            elif id == "Try other keywords":
                print("TRY OTHER KEYWORDS")
                tx = {"TryOtherKeywords": "Try other keywords"}

        tx["AnalyzedText"] = text_fin
        tx["snaphot_retrieval_time"] = int(time.time() - start)
        tx["snapshot_date_time"] = datetime.now()
        tx["snapshot_by"] = req_by

        print(tx)
        return tx
