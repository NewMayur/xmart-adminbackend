import base64
import uuid
import jwt
from functools import wraps
from flask import jsonify, request
from server import app


def save_base64_file(data):
    file_name = str(uuid.uuid4())
    banner_img_location = "./static/" + file_name
    with open(banner_img_location, "wb") as fh:
        base64_str = data
        base64_str = base64_str.split(",")[1] if "," in base64_str else base64_str

        missing_padding = len(base64_str) % 4
        if missing_padding != 0:
            base64_str += "=" * (4 - missing_padding)
        fh.write(base64.decodebytes(base64_str.encode("utf-8")))
    return file_name


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f({}, *args, **kwargs)

    return decorated
