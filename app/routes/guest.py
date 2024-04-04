from flask import request
from server import app
from app.extensions.db import db
from app.extensions.responses import response_base
from app.extensions.utils import token_required
import jwt


@app.route("/guest/auth", methods=["POST"])
def guest_room_auth():
    print(request.json)
    token = jwt.encode(
        {
            "room_number": request.json["room_number"],
            "floor_id": request.json["floor_id"],
            "building_id": request.json["building_id"],
        },
        app.config["JWT_SECRET_KEY"],
    )
    return response_base(message="Success", status=200, data=[])


@app.route("/guest/room/config", methods=["POST"])
@token_required
def load_room_config():
    return response_base(message="Success", status=200, data={})
