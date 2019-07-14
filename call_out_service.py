from flask_cors import CORS
from flask import Flask, render_template, request, redirect, send_from_directory, json, jsonify, send_file
import os
import json
import logging
logging.getLogger().setLevel(logging.INFO)

import config
from pyfcm import FCMNotification

template_dir = os.path.abspath('views')
app = Flask(__name__, template_folder=template_dir)
CORS(app)

def call2clients(registration_ids, call_center_code):
    push_service = FCMNotification(api_key=config.FCM_APIKEY)
    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        data_message={'phoneNumber': call_center_code})
    print(result)

# print(result)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html", clients=config.CLIENTS, call_centers=config.CALL_CENTERS)
    if request.method == 'POST':
        print(request.form)
        call_center_code = request.form['callCenter']
        registration_ids = []
        for id, name, token in config.CLIENTS:
            if id in request.form:
                registration_ids.append(token)
        if len(registration_ids) > 0:
            call2clients(registration_ids, call_center_code)
        return render_template("index.html", clients=config.CLIENTS, call_centers=config.CALL_CENTERS, success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6789)