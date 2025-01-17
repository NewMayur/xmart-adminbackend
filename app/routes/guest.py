import os

from flask import request, jsonify, make_response

from server import app, bcrypt
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
from app.schema.Building import Floor, Building
from app.schema.User import User
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
        response = jsonify({"token": token})
        response.headers["auth-token"] = token
        return response
        # return response_base(message="Success", status=200, data=[{"token": token}]).headers['auth-token'] = token
    else:
        return response_base(message="Failed", status=404)


@app.route("/guest/room/config", methods=["POST"])
# @jwt_required()
def load_room_config():
    # current_user = get_jwt_identity()
    floor = Floor.query.filter_by(number=request.json["floor_number"]).first()
    if floor:
        room = Room.query.filter_by(number=request.json["room_number"]).first()
        if room == None:
            return response_base(message="Failed", status=404)
        else:
            pass
        room_devices = RoomDevice.query.filter_by(
            room_id=room.id,
            floor_id=floor.id,
            building_id=request.json["building_id"],
            is_published=1,
        ).all()

        final_data = {"device_data": [], "experience_data": []}
        for device in room_devices:
            print(device.is_service)
            final_config = {}
            print(json.loads(device.device_config))
            if not isinstance(
                json.loads(device.device_config), dict
            ):  # json.loads(device.device_config)
                for dev_con in json.loads(device.device_config):
                    print(dev_con)
                    final_config[dev_con["technical_name"]] = dev_con["address"]
            else:
                final_config = json.loads(device.device_config)
            final_data["device_data"].append(
                {
                    "id": device.id,
                    "name": device.name,
                    "add_to_home_screen": device.add_to_home_screen,
                    "sub_room": (
                        device.room_sub_type.name if device.room_sub_type else None
                    ),
                    "sub_room_technical": (
                        device.room_sub_type.technical_name
                        if device.room_sub_type
                        else None
                    ),
                    "device_sub_type": device.device_sub_type.name,
                    "device_sub_type_technical": device.device_sub_type.technical_name,
                    "device_type": device.device_type.name,
                    "device_type_technical": device.device_type.technical_name,
                    "protocol": device.protocol.name,
                    # "controls": json.loads(device.device_config),
                    "controls": final_config,
                    "icon": device.icon,
                    "floor_id": device.floor_id,
                    "building_id": device.building_id,
                    "room_id": device.room_id,
                    "room_number": device.room_number,
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
    else:
        return response_base(message="Failed", status=404)

@app.route("/guest/room/v2/config", methods=["POST"])
def load_room_v2_config():
    data = request.json
    building_id = data.get("building_id")
    floor_id = data.get("floor_id")
    room_id = data.get("room_id")
    password_input = data.get("admin_pass")

    # Password validation logic
    password_env = os.environ.get("ADMIN_PASSWORD")
    if password_input == password_env:
        token = create_access_token(
            identity={
                "building_id": request.json["building_id"],
                "floor_id": request.json["floor_id"],
                "room_id": request.json["room_id"]
            }
        )
        response = jsonify({"token": token})
        response.headers["auth-token"] = token

        room_devices = RoomDevice.query.filter_by(
            room_id=room_id,
            floor_id=floor_id,
            building_id=building_id
        ).all()
        final_data = {"device_data": []}
        for device in room_devices:
            final_config = {}
            if isinstance(json.loads(device.device_config), list):
                for dev_con in json.loads(device.device_config):
                    if isinstance(dev_con, dict):
                        if device.protocol_id == 1:
                            final_config[dev_con.get("technical_name", "")] = dev_con.get("object_instance", "")
                        else:
                            final_config[dev_con.get("technical_name", "")] = dev_con.get("address", "")
                    else:
                        print("Unexpected format in device configuration list")
            else:
                final_config = json.loads(device.device_config)

            final_data["device_data"].append({
                "id": device.id,
                "name": device.name,
                "add_to_home_screen": device.add_to_home_screen,
                "sub_room": (
                    device.room_sub_type.name if device.room_sub_type is not None else ""
                ),
                "sub_room_technical": (
                    device.room_sub_type.technical_name
                    if device.room_sub_type is not None
                    else ""
                ),
                "device_sub_type": device.device_sub_type.name,
                "device_sub_type_technical": device.device_sub_type.technical_name,
                "device_type": device.device_type.name,
                "device_type_technical": device.device_type.technical_name,
                "protocol": device.protocol.name,
                #"controls": json.loads(device.device_config),
                "controls": final_config,
                "icon": device.icon,
                "floor_id": device.floor_id,
                "building_id": device.building_id,
                "room_id": device.room_id,
                "room_number": device.room_number,
                "device_type_id": device.device_type_id,
                "device_sub_type_id": device.device_sub_type_id,
                "is_service": device.is_service,
            })

        if len(final_data["device_data"]) == 0:
            return response_base(message="No devices found in the room", status=404, data=final_data)
        else:
            return response_base(message="Success", status=200, data=final_data)
        # return response_base(message="Success", status=200, data=[{"token": token}]).headers['auth-token'] = token
    else:
        return response_base(message="Invalid Password", status=401,data=[])

@app.route("/guest/room/v3/config", methods=["POST"])
def load_room_v3_config():
    data = request.json
    building_id = data.get("building_id")
    floor_id = data.get("floor_id")
    room_id = data.get("room_id")
    password_input = data.get("admin_pass")

    # Password validation logic
    password_env = os.environ.get("ADMIN_PASSWORD")
    if password_input == password_env:
        token = create_access_token(
            identity={
                "building_id": request.json["building_id"],
                "floor_id": request.json["floor_id"],
                "room_id": request.json["room_id"]
            }
        )
        response = jsonify({"token": token})
        response.headers["auth-token"] = token

        room_devices = RoomDevice.query.filter_by(
            room_id=room_id,
            floor_id=floor_id,
            building_id=building_id
        ).all()
        
        final_data = {"device_data": {}}

        for device in room_devices:
            device_type_technical = device.device_type.technical_name
            device_sub_type_technical = device.device_sub_type.technical_name

            if device_type_technical not in final_data["device_data"]:
                final_data["device_data"][device_type_technical] = {}

            if device_sub_type_technical not in final_data["device_data"][device_type_technical]:
                final_data["device_data"][device_type_technical][device_sub_type_technical] = []

            final_config = {}
            if isinstance(json.loads(device.device_config), list):
                for dev_con in json.loads(device.device_config):
                    if isinstance(dev_con, dict):
                        if device.protocol_id == 1:
                            final_config[dev_con.get("technical_name", "")] = dev_con.get("object_instance", "")
                        else:
                            final_config[dev_con.get("technical_name", "")] = dev_con.get("address", "")
                    else:
                        print("Unexpected format in device configuration list")
            else:
                final_config = json.loads(device.device_config)

            final_data["device_data"][device_type_technical][device_sub_type_technical].append({
                "id": device.id,
                "name": device.name,
                "building_id": device.building_id,
                "controls": final_config,
                "add_to_home_screen": device.add_to_home_screen,
                "device_sub_type": device.device_sub_type.name,
                "device_sub_type_id": device.device_sub_type_id,
                "device_sub_type_technical": device_sub_type_technical,
                "device_type": device.device_type.name,
                "device_type_id": device.device_type_id,
                "device_type_technical": device_type_technical,
                "floor_id": device.floor_id,
                "icon": device.icon,
                "room_id": device.room_id,
                "room_number": device.room_number,
                "sub_room_id": device.room_sub_type.id if device.room_sub_type is not None else 0,
                "sub_room": device.room_sub_type.name if device.room_sub_type is not None else "",
                "sub_room_technical": device.room_sub_type.technical_name if device.room_sub_type is not None else "",
                "protocol": device.protocol.name,
                "is_service": device.is_service,
            })

        if len(final_data["device_data"]) == 0:
            return response_base(message="No devices found in the room", status=404, data=final_data)
        else:
            return response_base(message="Success", status=200, data=final_data)
        # return response_base(message="Success", status=200, data=[{"token": token}]).headers['auth-token'] = token
    else:
        return response_base(message="Invalid Password", status=401, data=[])

@app.route("/guest/room/v4/config", methods=["POST"])
def load_room_v4_config():
    data = request.json
    building_id = data.get("building_id")
    floor_id = data.get("floor_id")
    room_id = data.get("room_id")
    password_input = data.get("password")

    # Password validation logic
    user = User.query.filter_by(username=request.json["username"]).first()
    if (user is not None) and bcrypt.check_password_hash(
        user.password, password_input
    ):
        access_token = create_access_token(identity={"username": user.username})
        # Load room configuration
        room_devices = RoomDevice.query.filter_by(
            room_id=room_id,
            floor_id=floor_id,
            building_id=building_id
        ).all()
        final_data = {"device_data": [], "token" : access_token}
        for device in room_devices:
            final_config = {}
            if isinstance(json.loads(device.device_config), list):
                for dev_con in json.loads(device.device_config):
                    if isinstance(dev_con, dict):
                        final_config[dev_con.get("technical_name", "")] = dev_con.get("address", "")
                    else:
                        print("Unexpected format in device configuration list")
            else:
                final_config = json.loads(device.device_config)

            final_data["device_data"].append({
                "id": device.id,
                "name": device.name,
                "add_to_home_screen": device.add_to_home_screen,
                "sub_room": (
                    device.room_sub_type.name if device.room_sub_type else None
                ),
                "sub_room_technical": (
                    device.room_sub_type.technical_name
                    if device.room_sub_type
                    else None
                ),
                "device_sub_type": device.device_sub_type.name,
                "device_sub_type_technical": device.device_sub_type.technical_name,
                "device_type": device.device_type.name,
                "device_type_technical": device.device_type.technical_name,
                "protocol": device.protocol.name,
                #"controls": json.loads(device.device_config),
                "controls": final_config,
                "icon": device.icon,
                "floor_id": device.floor_id,
                "building_id": device.building_id,
                "room_id": device.room_id,
                "room_number": device.room_number,
                "device_type_id": device.device_type_id,
                "device_sub_type_id": device.device_sub_type_id,
                "is_service": device.is_service,
            })

        if len(final_data["device_data"]) == 0:
            return response_base(message="No devices found in the room", status=404, data=final_data)
        else:
            return response_base(message="Success", status=200, data=final_data)
        # return response_base(message="Success", status=200, data=[{"token": token}]).headers['auth-token'] = token
    else:
        return response_base(message="Invalid Password", status=403, data=[])



@app.route("/buildings-floors-rooms", methods=["GET"])
def get_buildings_floors_rooms():
    buildings = Building.query.all()
    if len(buildings) == 0:
        return response_base(message="No buildings found", status=404, data=[])

    building_data = []
    for building in buildings:
        building_info = {
            "building_id": building.id,
            "building_name": building.number if not building.name else f"{building.number} - {building.name}",
            "number_of_floors": building.number_of_floors,
            "property_id": building.property_id,
            "floors": []
        }

        # Fetch floors for each property
        floors = Floor.query.filter_by(building_id=building.id).all()
        for floor in floors:
            floor_info = {
                "floor_id": floor.id,
                "floor_name": floor.number if not floor.name else f"{floor.number} - {floor.name}",
                "rooms": [],
            }

            # Fetch rooms for each floor
            rooms = Room.query.filter_by(floor_id=floor.id).all()
            for room in rooms:
                room_info = {
                    "room_id": room.id,
                    "room_name": room.number if not room.name else f"{room.number} - {room.name}"
                }
                floor_info["rooms"].append(room_info)

            building_info["floors"].append(floor_info)

        building_data.append(building_info)

    return response_base(message="Success", status=200, data=building_data)

@app.route("/test1", methods=["GET"])
def get_buildings_floors_rums():
    buildings = Building.query.all()
    for building in buildings:
        print(building)
        for floor in building.floors:
            print(floor)
            print(floor.rooms)
    return response_base(message="Success", status=200, data=[])

@app.route("/admin-mode", methods=["POST"])
def admin_mode():
    student = User.query.filter_by(username=request.json["username"]).first()
    print(student)
    if (student is not None) and bcrypt.check_password_hash(
        student.password, request.json["password"]
    ):
        return response_base(message="Authenticated", status=200, data=[])
    else:
        return response_base(message="Incorrect credentials", status=403, data=[])