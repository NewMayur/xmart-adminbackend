from flask import request
from server import app
from app.extensions.db import db
from app.extensions.responses import response_base
from app.extensions.utils import token_required
import jwt
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from app.schema.Device import KnxDeviceSubTypeData


@app.route("/guest/auth", methods=["POST"])
def guest_room_auth():
    print(request.json)
    if request.json["admin_pass"] == "admin":
        token = create_access_token(
            identity={
                "room_number": request.json["room_number"],
                "floor_id": request.json["floor_id"],
                "building_id": request.json["building_id"],
            }
        )
        return response_base(message="Success", status=200, data=[{"token": token}])
    else:
        return response_base(message="Failed", status=404)


@app.route("/guest/room/config", methods=["POST"])
@jwt_required()
def load_room_config():
    current_user = get_jwt_identity()
    return response_base(message="Success", status=200, data=current_user)
