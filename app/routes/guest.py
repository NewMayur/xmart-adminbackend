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
    room = Room.query.filter_by(
        number=request.json["room_number"],
        floor_id=request.json["floor_id"],
        building_id=request.json["building_id"],
    ).all()
    print(room)
    if len(room) > 0:
        print(room[0].id)
        room_device = RoomDevice.query.filter_by(
            room_id=room[0].id,
        ).all()
        devices = {}
        if len(room_device) > 0 and room_device:

            final_devices = {
                "devices": {},
                "scenes": [],
                "services": [],
                "air_conditioner": [],
            }
            for device in room_device:
                print(device.is_service)
                print(device.device_sub_type)
                if device.is_service:
                    final_devices["services"].append(
                        {
                            "id": device.id,
                            "name": device.name,
                            "add_to_home_screen": device.add_to_home_screen,
                            "sub_room": device.room_sub_type.name,
                            "type": device.device_sub_type.name,
                            "knx": json.loads(device.device_config),
                            "icon": device.icon,
                            "bacnet": {},
                        }
                    )
                    continue
                if device.device_type.name not in devices.keys():
                    print("hello")
                    devices[device.device_type.name] = [
                        {
                            "id": device.id,
                            "name": device.name,
                            "add_to_home_screen": device.add_to_home_screen,
                            "sub_room": device.room_sub_type.name,
                            "type": device.device_sub_type.name,
                            "knx": json.loads(device.device_config),
                            "icon": device.icon,
                            "bacnet": {},
                        }
                    ]
                    # print(devices)
                else:
                    devices[device.device_type.name].append(
                        {
                            "id": device.id,
                            "name": device.name,
                            "add_to_home_screen": device.add_to_home_screen,
                            "type": device.device_sub_type.name,
                            "knx": json.loads(device.device_config),
                            "sub_room": device.room_sub_type.name,
                            "icon": device.icon,
                            "bacnet": {},
                        }
                    )
            final_devices["devices"].update(devices)
            # print(devices)
            return response_base(message="Success", status=200, data=final_devices)
        else:

            return response_base(message="Failure", status=404, data=[])
    else:
        return response_base(message="Failure", status=404, data=[])
