import json
import random
import time
from datetime import datetime
from random import shuffle

import pandas as pd
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



def clean_name(s):
    s = s.lower()
    s = re.sub('<.*?>', '', s)
    s = re.sub(r'\\.*', "", s)
    s = re.sub(r'\-.*', "", s)
    s = re.sub('[\(\[].*?[\)\]]', "", s)
    s = s.strip()
    s = re.sub("[^a-zA-Z]+", "", s)
    return s


# app = Flask(__name__)
# @app.route('/static/', methods=['GET'])
def ss(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token):
    with requests.session() as s:

        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = "\"" + csrf_token + "\""
        s.headers["csrf-token"] = csrf_token

        start = time.time()

        key_name = key_name.strip().lower()
        key_company = key_company.strip().lower()
        key_role = key_role.strip().lower()
        key = key_name.strip() + " " + key_company.strip() + " " + key_role.strip()

        print(req_by)
        print(pub_id)
        print(key_name)
        print(key_company)
        print(key_role)


        if pub_id != "" or key != "  ":
            print("pub_id-", pub_id)
            print("key-", key)

            if pub_id != "":
                info = dict(e.index(pub_id=pub_id, key="", s=s))
            elif key != "  ":
                info = dict(e.index(pub_id=pub_id, key=key, s=s))


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

            if clean_name(str(info["first_name"])) == "tryotherkeywords":
                print("FULL NAME NOT FOUND. TRYING FIRST NAME")
                if (len(key_name.split(" ")) > 1):
                    key = str(key_name.split(" ")[:-1][0]) + " " + key_company + " " + key_role
                else:
                    key = key_name + " " + key_company + " " + key_role

                info = dict(e.index(pub_id=pub_id, key=key, s=s))

            ##################################################################################################################################################################
            ##################################################################################################################################################################

            if pub_id != "":
                print("linkedin public handle given")
                tx = {"contact_info_linkedin": info,
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) == clean_name(
                    str(key_name).lower()):
                print("BOTH SAME")
                tx = {"contact_info_linkedin": info,
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()):
                print("BOTH DIFFERENT")
                tx = {"contact_info_linkedin": "LINKEDIN USER -" + str(key_name) + " NOT FOUND." ,
                      }

            elif key != "  " and clean_name(str(info["first_name"] + " " + info["last_name"]).lower()) != clean_name(
                    str(key_name).lower()):
                print("BOTH DIFFERENT AND NO TWITTER")
                tx = {"NoLinkedinFoundNoTwitterFound": "Couldn't find any information about -" + str(
                    key_name) + ". Please provide the first name, last name and company name of your contact."}
            elif pub_id == "" and key == "  ":
                print("NOTHING GIVEN")
                tx = {"NoDataGiven": "Please provide atleast the first name, last name and company name of your contact."}

            elif id == "Try other keywords":
                print("TRY OTHER KEYWORDS")
                tx = {"TryOtherKeywords": "Try other keywords"}


        tx["snaphot_retrieval_time"] = int(time.time() - start)
        tx["snapshot_date_time"] = datetime.now()
        tx["snapshot_by"] = req_by
        r.insert_one(tx)
        tx = json.loads(json.dumps(tx, default=str))
        tx.popitem()


    if list(tx.keys())[0] == "NoLinkedinFoundNoTwitterFound":
        fin = tx
    else:
        if tx["contact_info_linkedin"] != "":

            if tx["contact_info_linkedin"] != "LINKEDIN USER NOT FOUND. USING ONLY TWITTER" and tx[
                "contact_info_linkedin"] != "USING ONLY TWITTER":
                l_han = tx["contact_info_linkedin"]["linkedin_handle"]
                c_desig = tx["contact_info_linkedin"]["current_company"]["detail"]["title"]
                c_comp = tx["contact_info_linkedin"]["current_company"]["name"]


            else:
                l_han = tx["contact_info_linkedin"]["linkedin_handle"]
                c_desig = tx["contact_info_linkedin"]["current_company"]["detail"]["title"]
                c_comp = tx["contact_info_linkedin"]["current_company"]["name"]

            f_name = info["first_name"]
            l_name = info["last_name"]
            curr_snap = tx["snapshot_date_time"]
            by = tx["snapshot_by"]
            retr = tx["snaphot_retrieval_time"]

        else:
            l_han = ""
            f_name = ""
            l_name = ""
            c_desig = ""
            c_comp = ""
            curr_snap = ""
            by = ""
            retr = ""

        fin = {"LinkedInHandle": l_han, "First_Name": f_name, "Last_Name": l_name,
               "Contact_Current_Designation": c_desig,
               "Contact_Current_Company": c_comp, "snapshot_static_date_time": curr_snap,
               "snapshot_staic_requestedby": by, "snaphot_static_retrieval_time": retr
               }

    print(fin)
    return fin


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)