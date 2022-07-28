# email = "maharajsoorya@gmail.com"
# pswd = "soor1234"
#
# c = client.Client()
# cookie = dict(c._do_authentication_request(username=email, password=pswd))
# li_at = cookie["li_at"]
# csrf_token = cookie["JSESSIONID"][1:-1]

from flask import Flask, request
import static_dynamic as sd
import dynamic as d
import static_final as s
import manualText as m

app = Flask(__name__)
@app.route('/dynamicApi/', endpoint='dynamicApi', methods=["POST", "GET"])
@app.route('/staticApi/', endpoint='staticApi', methods=["POST", "GET"])
@app.route('/staticDynamicApi/', endpoint='staticDynamicApi', methods=["POST", "GET"])
@app.route('/manualApi/', endpoint='manualApi', methods=["POST", "GET"])


def index():

    liu = request.args['liu']
    req_by = request.args['req_by']
    pub_id = request.args['pub_id']
    key_name = request.args['key']
    key_company = request.args['comp']
    key_role = request.args['role']
    twitter_id = request.args['twitter_id']
    li_at = request.args['li_at']
    csrf_token = request.args['jsession'][1:-1]

    # static,dynamic, static_dynamic, manual_text
    # http://127.0.0.1:5000/staticDynamicApi/?liu=sudipdutta&req_by=Sudip%20Dutta&pub_id=&key=Sudip%20Dutta&comp=Relatas&role=&twitter_id=&li_at=AQEDAR3w60MBg6ubAAABfXbXBS4AAAGAQUomE00AdW1NOtA2cQeKDUtZWZb0N3euSOMHWmHPjnirndIM2YFjZL0zhdFjf7juukQ70svIa01MvKuP_qV_HsXD31VVSj3WG5r-4i6ZrJ5bCwXoZiyKfB5w&jsession="ajax:1095510188571782066"&text=
    
    if li_at == "" or csrf_token == "":
        msg = {"SessionExpired": "Reload the page!"}
    else:
        if request.endpoint == 'staticDynamicApi':
            msg = sd.aa(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token)

        elif request.endpoint == 'dynamicApi':
            msg = d.dd(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token)

        elif request.endpoint == 'staticApi':
            msg = s.ss(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token)

        elif request.endpoint == 'manualApi':
            text = request.args['text']
            msg = m.index(liu, req_by, pub_id, key_name, key_company, key_role, twitter_id, li_at, csrf_token, text)

        else:
            msg = {"UnknownEndpoint": "Passed an endpoint that doesn't exist!"}

    # print(msg)
    return msg


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)