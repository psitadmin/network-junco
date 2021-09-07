from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import DBAPIError
from login import login
from devices.devices_db import *
from devices.devices_connection import get_device_config
from arp_service.calambuco import search_calambuco
from arp_service.arp_db import get_transit_interfaces, transit_interfaces_controller #, post_transit_interfaces, delete_transit_interfaces, update_transit_interfaces
import os
import json
from tasks.interfacesTask import get_device_interfaces, post_interface_config


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["CORS_HEADERS"] = "Content-Type"

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# ========================================================================
# DEVICES SERVICE
# ==============================================q==========================
@app.route("/devices", methods=["GET", "DELETE", "PUT", "POST"])
@cross_origin()
def devices():
    response = {}
    try:
        if request.method == "GET":
            if(request.args.get('device')):
                dev = get_device_by_id(request.args.get('device'))
                response["data"] = get_device_id_json(dev)
                response["status"] = "success"
            else:
                response["data"] = get_devices_json()
                response["status"] = "success"
        if request.method == "DELETE":
            devices_delete = request.get_json()
            devices_ids = []
            for device in devices_delete["devices"]:
                devices_ids.append(device["id"])
            delete_devices(devices_ids)
            response["status"] = "success"
        if request.method == "POST":
            device = request.get_json()["data"]["device"]
            add_device(device)
            response["status"] = "success"
        if request.method == "PUT":
            device = request.get_json()["data"]["device"]
            edit_device(device)   

        return jsonify(response), 200

    except DBAPIError as e:
        print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        return jsonify(response), 500

@app.route("/devices/config", methods=["POST"])
@cross_origin()
def device_config():
    response = {}
    try:
        if request.method == "POST":
            response["data"] = get_device_config(request.get_json()["data"]["device"] )
            response["status"] = "success"
            return jsonify(response), 200
        else:
            return 405

    except TypeError as te:
        error = (get_device_config(request.get_json()["data"]["device"]))
        response["data"] = str(error)
        response["status"] = "fail"
        return(response,500)

    except Exception as e:
        print("RESPONSE => type( ", type(e), ") :\n", e)
        response["data"] = str(e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        raise Exception
# ========================================================================

# ========================================================================
# TASK SERVICE
# ========================================================================
@app.route("/task/interfaces", methods=["GET", "POST"])
@cross_origin()
def interfaces():
    response = {}
    try:
        if request.method == "GET":
            response["data"] = get_device_interfaces(request.args.get('device'))
            response["status"] = "success"
            return jsonify(response), 200
        if request.method == "POST":
            dev = request.args.get('device')
            result = post_interface_config(dev, request.get_json()["data"]["changes"])
            response["status"] = "success"
            return jsonify(result), 200
    except Exception as e:
        print("RESPONSE => type( ", type(e), ") :\n", e)
        response["data"] = str(e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        raise Exception
# ========================================================================


# ========================================================================
# ARP SERVICE
# ========================================================================
@app.route("/arp", methods=["POST"])
@cross_origin()
def arp():
    response = {}
    try:
        if request.method == "POST":
            to_search = request.get_json()["data"]["address"]
            result = search_calambuco(to_search)
            # print("Dato: {0}\nREsultado: {1}".format(to_search, result))
            if(result):
                # print("ARP RESULT ES == ", result)
                return jsonify(result), 200
            else:
                return "Invalid format", 400

    except Exception as e:
        # print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        print(e)
        return jsonify(response), 500
@app.route("/arp/transitinterfaces", methods=["GET", "POST"])
@cross_origin()
def arp_transit_interfaces():
    response = {}
    try:
        if request.method == "GET":
            result = get_transit_interfaces()
            if(result):
                return jsonify(result), 200
            else:
                return "Invalid format", 400
        if request.method == "POST":
            new_int = request.get_json()["data"]["put"]
            delete_int = request.get_json()["data"]["delete"]
            edit_int = request.get_json()["data"]["post"]

            result = transit_interfaces_controller(new_int, delete_int, edit_int)
            if(result):
                return jsonify(result), 200
            else:
                return "Invalid format", 400
    except Exception as e:
        # print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        print(e)
        return jsonify(response), 500
# ========================================================================

@app.route("/devices/vendors", methods=["GET"])
@cross_origin()
def device_vendors():
    response = {}
    try:
        if request.method == "GET":
            response["data"] = get_vendors()
            response["status"] = "success"
        return jsonify(response), 200

    except DBAPIError as e:
        # print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        return jsonify(response), 500

@app.route("/devices/protocol", methods=["GET"])
@cross_origin()
def device_protocols():
    response = {}
    try:
        if request.method == "GET":
            response["data"] = get_protocols()
            response["status"] = "success"
        return jsonify(response), 200

    except DBAPIError as e:
        # print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        return jsonify(response), 500

@app.route("/devices/device_types", methods=["GET"])
@cross_origin()
def device_types():
    response = {}
    try:
        if request.method == "GET":
            response["data"] = get_device_types()
            response["status"] = "success"
        return jsonify(response), 200

    except DBAPIError as e:
        # print("RESPONSE => type( ", type(e), ") :\n", e)
        response["status"] = "fail"
        response["encoding_errors"] = str(e)
        return jsonify(response), 500

@app.route("/login", methods=["POST"])
@cross_origin()
def login_authentication():
    """ Call method for authentication """
    # Retrieves data from response object
    user = request.authorization.get("username")
    password = request.authorization.get("password")

    # Send the auth credentials to login server
    response_status = app.response_class(status=login.request_auth(user, password))
    # print (response_status)

    return response_status


if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV")
    # app.config["APPLICATION_ROOT"] = 'asdf:5000'
    # app.config["SERVER_NAME"] = 'localhosta:5000'
    # pr-junco-1-mad.hi.inet
    print("environment ======= ", env)
    if(env=="development"):
        app.run(host="10.95.245.72", debug= True)
    elif(env=="production"):
        print("ENTRA EN PRO")
        app.run(host="10.95.245.68", ssl_context='adhoc', debug=False)
    elif(env=="docker"):
        app.run(host="0.0.0.0")
    else:
        app.run(host="0.0.0.0")
