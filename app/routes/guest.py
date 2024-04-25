from flask import request
from server import app
from app.extensions.db import db
from app.extensions.responses import response_base
from app.extensions.utils import token_required
from app.schema.Room import RoomDevice, Room
import jwt
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from app.schema.Device import KnxDeviceSubTypeData
import json
import ast


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
# @jwt_required()
def load_room_config():
    # current_user = get_jwt_identity()
    room_devices = RoomDevice.query.filter_by(
        room_number=request.json["room_number"],
        floor_id=request.json["floor_id"],
        building_id=request.json["building_id"],
    ).all()

    final_data = {"device_data": [], "experience_data": []}
    for device in room_devices:
        print(device.is_service)
        final_data["device_data"].append(
            {
                "id": device.id,
                "name": device.name,
                "add_to_home_screen": device.add_to_home_screen,
                "sub_room": device.room_sub_type.name,
                "device_sub_type": device.device_sub_type.name,
                "device_type": device.device_type.name,
                "protocol": device.protocol.name,
                "controls": json.loads(device.device_config),
                "icon": device.icon,
                "floor_id": device.floor_id,
                "building_id": device.building_id,
                "room_id": device.room_id,
                "room_number": device.room_number,
                # "device_make": device.device_make,
                # "device_model": device.device_model,
                "device_type_id": device.device_type_id,
                "device_sub_type_id": device.device_sub_type_id,
                "is_service": device.is_service,
            }
        )
    return response_base(
        message="Success",
        status=200,
        data=final_data,
    )
