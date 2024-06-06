from flask import request, jsonify, make_response

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
from app.schema.Building import Floor, Building
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

@app.route("/guest/room/v1/config", methods=["POST"])
def load_room_v1_config():
    data = request.json
    building_id = data.get("building_id")
    floor_id = data.get("floor_id")
    room_id = data.get("room_id")
    password = data.get("password")

    # Password validation logic

    room = Room.query.filter_by(id=room_id).first()
    if room:
        print(room_id,floor_id,building_id)
        room_devices = RoomDevice.query.filter_by(
            room_id=room_id,
            floor_id=floor_id,
            building_id=building_id
        ).all()
        print(room_devices)
        final_data = {"device_data": []}
        for device in room_devices:
            final_config = json.loads(device.device_config)
            if not isinstance(final_config, dict):
                    final_config = {dev_con["technical_name"]: dev_con["address"] for dev_con in final_config}

            final_data["device_data"].append({
                "id": device.id,
                "name": device.name,
                "add_to_home_screen": device.add_to_home_screen,
                "sub_room": device.room_sub_type.name if device.room_sub_type else None,
                "sub_room_technical": device.room_sub_type.technical_name if device.room_sub_type else None,
                "device_sub_type": device.device_sub_type.name,
                "device_sub_type_technical": device.device_sub_type.technical_name,
                "device_type": device.device_type.name,
                "device_type_technical": device.device_type.technical_name,
                "protocol": device.protocol.name,
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

        return response_base(message="Success", status=200, data=final_data)
    else:
        return response_base(message="Failed", status=404)

@app.route("/buildings-floors-rooms", methods=["GET"])
def get_buildings_floors_rooms():
    buildings = Building.query.all()
    if len(buildings) == 0:
        return response_base(message="No buildings found", status=404, data=[])

    building_data = []
    for building in buildings:
        building_info = {
            "building_id": building.id,
            "building_name": f"{ building.number } - { building.name }",
            "number_of_floors": building.number_of_floors,
            "property_id": building.property_id,
            ""
            "floors": []
        }

        # Fetch floors for each property
        floors = Floor.query.filter_by(building_id=building.id).all()
        for floor in floors:
            floor_info = {
                "floor_id": floor.id,
                "floor_name": f"{floor.number} - {floor.name}",
                "rooms": [],
            }

            # Fetch rooms for each floor
            rooms = Room.query.filter_by(floor_id=floor.id).all()
            for room in rooms:
                room_info = {
                    "room_id": room.id,
                    "room_name": f"{room.number} - {room.name}"
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