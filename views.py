from flask import make_response
from flask import request
from flask import abort
from flask import render_template
from flask import jsonify

import json
import os
import logging
import sys
import requests
import re

from app import app
import pickle
import pandas



def json_dumper(obj):
    """
    if the obj has a to_dict() function we've implemented, uses it to get dict.
    from http://stackoverflow.com/a/28174796
    """
    try:
        return obj.to_dict()
    except AttributeError:
        return obj.__dict__


def json_resp(thing):
    json_str = json.dumps(thing, sort_keys=True, default=json_dumper, indent=4)

    if request.path.endswith(".json") and (os.getenv("FLASK_DEBUG", False) == "True"):
        print u"rendering output through debug_api.html template"
        resp = make_response(render_template(
            'debug_api.html',
            data=json_str))
        resp.mimetype = "text/html"
    else:
        resp = make_response(json_str, 200)
        resp.mimetype = "application/json"
    return resp


def abort_json(status_code, msg):
    body_dict = {
        "HTTP_status_code": status_code,
        "message": msg,
        "error": True
    }
    resp_string = json.dumps(body_dict, sort_keys=True, indent=4)
    resp = make_response(resp_string, status_code)
    resp.mimetype = "application/json"
    abort(resp)


@app.after_request
def after_request_stuff(resp):
    #support CORS
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    resp.headers['Access-Control-Allow-Headers'] = "origin, content-type, accept, x-requested-with"

    # without this jason's heroku local buffers forever
    sys.stdout.flush()

    return resp






# ENDPOINTS
#
######################################################################################


@app.route('/', methods=["GET"])
def index_endpoint():
    return jsonify({
        "version": "0.1",
        "name": "api-starter-kit",
        "description": "Summary goes here.",
        "documentation_url": "none yet",
        "msg": "Don't panic"
    })

@app.route('/model', methods=['POST'])
def predict():
    input_ = request.get_json()
    column_list = ['Week_no''Agent_ID''Channel_ID''Sales_route','Client_ID','Product_ID']
    if not input_:
        return jsonify({
        "version": "0.1",
        "success": "0",
        "reason": "No JSON detected.",
    })
    for i in column_list:
        if i not in input_.keys():
            return jsonify({
                 "version": "0.1",
                 "success": "0",
                 "reason": "Invalid Columns detected.",
                  })
    else:
        loaded_model = None
        with open('/home/lekanterragon/Desktop/RazaqMLAPI/now.pickle','rb') as f:
            loaded_model = pickle.load(f)


        ####Clean this place up and do whatever you want to do here.

        predictions = loaded_model.predict(test)
        prediction_series = list(pd.Series(predictions))

        final_predictions = pd.DataFrame(list(prediction_series))
        responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        responses.status_code = 200

        return (responses)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)

















