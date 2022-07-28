# from linkedin_api import client
# email = "jimmytestacc@gmail.com"
# pswd = "naveen9972"
# c = client.Client()
# cookie = dict(c._do_authentication_request(username=email, password=pswd))
# print(cookie["li_at"])
# print(cookie["JSESSIONID"])

import warnings

warnings.filterwarnings("ignore")
import requests
from urllib.parse import urlencode

headers = {}


def search_profile(key, s):
    default_params = {"count": "1", "filters": "List()", "origin": "GLOBAL_SEARCH_HEADER", "q": "all", "start": 0,
                      "queryContext": "List(spellCorrectionEnabled->true,relatedSearchesEnabled->true,kcardTypes->PROFILE|COMPANY)",
                      "keywords": key}
    search = 'https://www.linkedin.com/voyager/api/search/blended?' + urlencode(default_params, safe='(),')
    sea = s.get(search)
    # print("SEARCH", sea)

    sea = sea.json()
    try:
        id = sea["elements"][0]["elements"][0]["image"]["attributes"][0]["miniProfile"]["publicIdentifier"]
        return {"id": id, "total_profiles": str(sea['metadata']['totalResultDisplayText']['text']).split()[0]}
    except:
        return "try other keywords!!"


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
        last_name = profile['profile']['lastName']
    except:
        last_name = ""
    try:
        first_name = profile['profile']['firstName']
    except:
        first_name = ""
    try:
        headline = profile['profile']['headline']
    except:
        headline = ""
    try:
        location = profile['profile']['geoLocationName']
    except:
        location = ""
    try:
        country = profile['profile']['geoCountryName']
    except:
        country = ""

    return {"urn": urn, "first_name": first_name, "last_name": last_name, "location": location,
            "country": country, "headline": headline,
            "about": about}


def jobs(public_id, s):
    complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
    profile = s.get(complete_profile)
    profile = profile.json()
    company = []
    for i in profile['positionGroupView']['elements']:
        for j in i["positions"]:
            try:
                n = j["companyName"]
            except KeyError:
                n = ""

            try:
                t = j["title"]
            except KeyError:
                t = ""

            try:
                tm = j["timePeriod"]
            except KeyError:
                tm = ""

            pos = {"name": n, "detail": {"title": t, "timePeriod": tm}}
            company.append(pos)

    if len(company) == 0:
        company.append({"name": "", "detail": {"title": "", "timePeriod": ""}})
        return company
    else:
        return company


def education_info(public_id, s):
    complete_profile = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileView'
    profile = s.get(complete_profile)
    profile = profile.json()

    education = []
    for i in profile['educationView']['elements']:
        try:
            n = i["schoolName"]
        except KeyError:
            n = ""

        try:
            d = i["degreeName"]
        except KeyError:
            d = ""

        try:
            f = i["fieldOfStudy"]
        except KeyError:
            f = ""

        try:
            t = i["timePeriod"]
        except KeyError:
            t = ""

        ed = {"name": n, "detail": {"degreeName": d, "fieldOfStudy": f, "timePeriod": t}}
        education.append(ed)

    if len(education) == 0:
        education.append({"name": "", "detail": {"degreeName": "", "fieldOfStudy": "", "timePeriod": ""}})
        return education
    else:
        return education


def article_info(public_id, s):
    posts = "https://www.linkedin.com/voyager/api/identity/profiles/" + public_id + "/posts"
    posts = s.get(posts)
    posts = posts.json()
    # print(posts)
    post = []

    for i in posts["elements"]:

        try:
            a = i["contentText"]["text"]
        except KeyError:
            a = ""
            # continue

        try:
            d = i["postedDate"]
        except KeyError:
            d = ""
            # continue

        try:
            u = i["permaLink"]
        except KeyError:
            u = ""
            # continue

        try:
            l = i["numLikes"]
        except KeyError:
            l = ""
            # continue

        try:
            cmt = i["numComments"]
        except KeyError:
            cmt = ""
            # continue

        post.append({"post": a, "time_period": d, "url": u, "num_cmt": cmt, "num_like": l})

    if len(post) == 0:
        post.append({"post": "", "time_period": "", "url": "", "num_cmt": "", "num_like": ""})
        return post
    else:
        return post


def posts_info(urn, s):
    # print("INSIDE POSTS")
    url_params = {
        "count": 100,
        "start": 0,
        "q": "memberShareFeed",
        "moduleKey": "member-shares:phone",
        "includeLongTermHistory": True,
        "profileUrn": urn
    }

    posts = "https://www.linkedin.com/voyager/api/identity/profileUpdatesV2?" + urlencode(url_params, safe='(),')

    posts = s.get(posts)
    posts = posts.json()
    p = []
    t = ""
    po = ""
    u = ""
    cmt = ""
    l = ""

    for i in posts["elements"]:
        try:
            u = i["updateMetadata"]["updateActions"]["actions"][1]["url"]
            # print("URL - ", u)
        except KeyError:
            u = ""

        try:
            t = i["actor"]["subDescription"]["accessibilityText"]
        except KeyError:
            t = ""

        try:
            po = i["commentary"]["text"]["text"]
        except KeyError:
            po = ""


        try:
            cmt = i["socialDetail"]["totalSocialActivityCounts"]["numComments"]
        except KeyError:
            cmt = ""

        try:
            l = i["socialDetail"]["totalSocialActivityCounts"]["numLikes"]
        except KeyError:
            l = ""

        p.append({"time_period": t, "post": po, "url": u, "num_cmt": cmt, "num_like": l})

    if len(p) == 0:
        # print("HELLO")
        p.append({"time_period": t, "post": po, "url": u, "num_cmt": cmt, "num_like": l})
        return p
    else:
        return p


def contacts(public_id, s):
    contact = 'https://www.linkedin.com/voyager/api/identity/profiles/' + public_id + '/profileContactInfo'
    cont = s.get(contact)
    cont = cont.json()

    try:
        e = cont.get("emailAddress")
    except:
        e = ""

    try:
        t = cont.get("twitterHandles")[0]["name"]
        tu = "https://twitter.com/" + t
    except:
        t = ""
        tu = ""

    try:
        ph = cont.get("phoneNumbers", [])
    except:
        ph = ""

    contact_info = {
        "email_address": e,
        "twitter": t,
        "twitter_url": tu,
        "phone_numbers": ph,
    }

    return contact_info


def index(pub_id, key, s):
    id = {"id": "", "total_profiles": 1}
    if pub_id == '' and key != '':
        # print("ENDPOINT-1 KEY PASSED")
        id = search_profile(key, s)

        try:
            pub_id = id["id"]
        except TypeError:
            return {"linkedin_handle": "Try other keywords",
                "linkedin_url": "Try other keywords",
                "total_profiles": "Try other keywords",
                "first_name": "Try other keywords",
                "last_name": "Try other keywords",
                "headline": "Try other keywords",
                "about": "Try other keywords",
                "location": {"city": "Try other keywords", "state": "Try other keywords", "country": "Try other keywords"},
                "email": "Try other keywords",
                "phone_number": "Try other keywords",
                "twitter": "Try other keywords",
                "twitter_url": "Try other keywords",
                "companies": "Try other keywords",
                "latest_linkedin_post": "Try other keywords",
                "schools": "Try other keywords",
                "all_posts": "Try other keywords",
                }

    elif pub_id == '' and key == '':
        return {"linkedin_handle": "Try other keywords",
                "linkedin_url": "Try other keywords",
                "total_profiles": "Try other keywords",
                "first_name": "Try other keywords",
                "last_name": "Try other keywords",
                "headline": "Try other keywords",
                "about": "Try other keywords",
                "location": {"city": "Try other keywords", "state": "Try other keywords",
                             "country": "Try other keywords"},
                "email": "Try other keywords",
                "phone_number": "Try other keywords",
                "twitter": "Try other keywords",
                "twitter_url": "Try other keywords",
                "companies": "Try other keywords",
                "latest_linkedin_post": "Try other keywords",
                "schools": "Try other keywords",
                "all_posts": "Try other keywords",
                }

    if pub_id == "try other keywords!!":
        return {"linkedin_handle": "Try other keywords",
                "linkedin_url": "Try other keywords",
                "total_profiles": "Try other keywords",
                "first_name": "Try other keywords",
                "last_name": "Try other keywords",
                "headline": "Try other keywords",
                "about": "Try other keywords",
                "location": {"city": "Try other keywords", "state": "Try other keywords",
                             "country": "Try other keywords"},
                "email": "Try other keywords",
                "phone_number": "Try other keywords",
                "twitter": "Try other keywords",
                "twitter_url": "Try other keywords",
                "companies": "Try other keywords",
                "latest_linkedin_post": "Try other keywords",
                "schools": "Try other keywords",
                "all_posts": "Try other keywords",
                }
    try:
        personal = personal_info(pub_id, s)
    except:
        return {"too_many_requests": "made more than 30 requests continuously"}

    try:
        company = jobs(pub_id, s)
    except:
        company = [""]

    try:
        education = education_info(pub_id, s)
    except:
        education = [""]

    try:
        contact_info = contacts(pub_id, s)
    except:
         contact_info = ""

    try:
        total_profiles = id["total_profiles"]
    except:
        total_profiles = ""

    try:
        f_name = personal["first_name"]
    except:
        f_name = ""

    try:
        l_name = personal["last_name"]
    except:
        l_name = ""

    try:
        headline = personal["headline"]
    except:
        headline = ""

    try:
        about = personal["about"]
    except:
        about = ""

    try:
        city = personal["location"].split(",")[0].strip()
    except IndexError:
        city = ""
    try:
        state = personal["location"].split(",")[1].strip()
    except IndexError:
        state = ""
    try:
        country = personal["country"]
    except IndexError:
        country = ""
    try:
        email = contact_info["email_address"]
    except:
        email = ""
    try:
        ph_no = contact_info["phone_numbers"]
    except:
        ph_no = ""
    try:
        twitter = contact_info["twitter"]
    except:
        twitter = ""
    try:
        twitter_url = contact_info["twitter_url"]
    except:
        twitter_url = ""
    try:
        post = posts_info(personal["urn"], s)
        if post[0] == "":
            # print("ARTICLE")
            post = article_info(pub_id, s)
    except:
        post = [""]


    linkedin_url = "https://www.linkedin.com/in/" + pub_id

    # print("Company-", company)

    endpoint = {"linkedin_handle": pub_id.strip().lower(),
                "linkedin_url": linkedin_url,
                "profile_confidence": int((1/int(str(total_profiles).replace(',', '')))*100),
                "first_name": f_name,
                "last_name": l_name,
                "headline": headline,
                "about": about,
                "location": {"city": city, "state": state, "country": country},
                "email": email,
                "phone_number": ph_no,
                "twitter": twitter,
                "twitter_url": twitter_url,
                "companies": company,
                "current_company": company[0],
                "latest_linkedin_post": post[0],
                "schools": education,
                "all_posts": post,
                }
    print("INSIDE ENDPOINT-1")
    return endpoint