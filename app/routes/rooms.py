from flask import current_app, request

from app.extensions.db import db
from app.extensions.responses import response_base
from app.schema.Building import Building, Floor
from app.schema.Room import Room, RoomDevice, RoomDeviceType, RoomRoomSubType
from server import app
import json

"""
    A function to create a new room in the database based on the provided JSON data.
    
    This function iterates over the JSON data to create a new Room object with associated device types and sub room types. 
    It then commits the changes to the database and returns a success response with the created room IDs if successful. 
    If an exception occurs during the process, it rolls back the session and returns a server error response.
"""


@app.route("/room/create", methods=["POST"])
def create_room():
    building_id = None
    floor_id = None
    room_number_list = []
    for room in request.json:
        building_id = room["building_id"]
        floor_id = room["floor_id"]
        room_number_list.append(room["number"])
    dupicate_room_check = (
        Room.query.filter(Room.number.in_(room_number_list))
        .filter(Room.building_id == building_id)
        .filter(Room.floor_id == floor_id)
        .all()
    )

    if len(dupicate_room_check) > 0:
        duplicate_data = []
        for data in dupicate_room_check:
            duplicate_data.append({"number": data.number, "name": data.name})
        return response_base(message="Failed", status=409, data=duplicate_data)
    created_room_ids = []
    try:
        # print(request.json)
        for room in request.json:
            # print(room)
            room_new = Room(
                name=room["name"],
                number=room["number"],
                property_id=room["property_id"],
                building_id=room["building_id"],
                floor_id=room["floor_id"],
                room_type_id=room["room_type_id"],
            )
            db.session.add(room_new)
            db.session.flush()
            created_room_ids.append(room_new.id)
            print(room["device_types"])
            for device in room["device_types"]:
                room_device_type = RoomDeviceType(
                    room_id=room_new.id, device_type_id=device
                )
                db.session.add(room_device_type)
            for sub_room in room["sub_room_type_ids"]:
                room_sub_type = RoomRoomSubType(
                    room_id=room_new.id,
                    room_sub_type_id=sub_room,
                )
                db.session.add(room_sub_type)
        db.session.commit()
        return response_base(
            message="Success", status=200, data=[{"ids": created_room_ids}]
        )
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


"""
Get the list of rooms for a given floor and return the room details including id, name, number, building, room type, and sub-room types.
"""


@app.route("/floor/room/list", methods=["POST"])
def get_room():
    floor = Floor.query.get_or_404(request.json["floor_id"])
    # print(building.floors)
    final_data = []
    for room in floor.rooms:
        final_data.append(
            {
                "id": room.id,
                "name": room.name,
                "number": room.number,
                "building": room.buildings.name,
                "room_type": room.room_type.name,
                "sub_room_types": [subtype.name for subtype in room.room_sub_types],
            }
        )

    return response_base(message="Success", status=200, data=final_data)


"""
    Retrieves a room from the database based on the provided room ID in the request JSON.
    
    Returns:
        - If the room is found, returns a JSON response with the room details including the room name, number, room type, floor, building, sub room types, and device types.
        - If the room is not found, returns a JSON response with a failure message and a status code of 404.
"""


@app.route("/room/view", methods=["POST"])
def view_room():
    room = Room.query.get_or_404(request.json["room_id"])
    if room is not None:
        room = {
            "name": room.name,
            "number": room.number,
            "room_type": {"name": room.room_type.name, "id": room.room_type.id},
            "floor": {"name": room.floors.name, "id": room.floors.id},
            "building": {"name": room.buildings.name, "id": room.buildings.id},
            "sub_room_types": [
                {"name": subtype.name, "id": subtype.id}
                for subtype in room.room_sub_types
            ],
            "device_types": [
                {"id": device.id, "name": device.name}
                for device in room.room_device_types
            ],
        }
        return response_base(message="Success", status=200, data=[room])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/config/view", methods=["POST"])
def room_config_view():
    room = Room.query.filter_by(
        number=request.json["room_number"],
        building_id=request.json["building_id"],
        floor_id=request.json["floor_id"],
    ).first()
    if room is not None:
        room = {
            "room_type": {"name": room.room_type.name, "id": room.room_type.id},
            "sub_room_types": [
                {"name": subtype.name, "id": subtype.id}
                for subtype in room.room_sub_types
            ],
            "device_types": [
                {"id": device.id, "name": device.name}
                for device in room.room_device_types
            ],
        }
        return response_base(message="Success", status=200, data=[room])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/edit", methods=["POST"])
def edit_room():
    print(request.json)
    room = Room.query.get_or_404(request.json["room_id"])
    if room is not None:
        # update device types
        for device in request.json["device_types_insert"]:
            room_device_type = RoomDeviceType(room_id=room.id, device_type_id=device)
            db.session.add(room_device_type)
        for device in request.json["device_types_delete"]:
            room_device_type = RoomDeviceType.query.filter_by(
                room_id=room.id, device_type_id=device
            ).first()
            db.session.delete(room_device_type)
        # Update subroom types
        for subroom in request.json["sub_room_types_insert"]:
            room_sub_type = RoomRoomSubType(room_id=room.id, room_sub_type_id=subroom)
            db.session.add(room_sub_type)
        for subroom in request.json["sub_room_types_delete"]:
            room_sub_type = RoomRoomSubType.query.filter_by(
                room_id=room.id, room_sub_type_id=subroom
            ).first()
            db.session.delete(room_sub_type)
        room.name = request.json["name"]
        room.number = request.json["number"]
        room.room_type_id = request.json["room_type_id"]
        room.floor_id = request.json["floor_id"]
        db.session.commit()
        return response_base(message="Success", status=200, data=[])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/add", methods=["POST"])
def add_device_to_room():
    print(request.json)
    room = Room.query.get_or_404(request.json["room_id"])
    if room is not None:
        print(request.json)
        room_device = RoomDevice(
            room_id=room.id,
            floor_id=request.json["floor_id"],
            building_id=request.json["building_id"],
            device_type_id=request.json["device_type_id"],
            device_sub_type_id=request.json["sub_device_type_id"],
            room_sub_type_id=request.json["sub_room_type_id"],
            is_published=request.json["is_published"],
            add_to_home_screen=request.json["add_to_home_screen"],
            icon=request.json["icon"],
            remark=request.json["remark"],
            protocol_id=request.json["protocol_id"],
            name=request.json["device_name"],
            group_name=request.json["device_group_name"],
            is_group=request.json["is_multiple"],
            is_service=request.json["is_service"],
            device_make=request.json["device_make"],
            device_model=request.json["device_model"],
            device_config=json.dumps(request.json["device_config"]),
            room_number=room.number,
        )
        db.session.add(room_device)
        db.session.commit()
        return response_base(
            message="Success", status=200, data=[{"id": room_device.id}]
        )
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/delete", methods=["DELETE"])
def delete_device_from_room():
    # print(request.json)
    room_device = RoomDevice.query.filter_by(
        id=request.json["device_id"], room_id=request.json["room_id"]
    )
    if room_device is not None:
        room_device.delete()
        db.session.commit()
        return response_base(message="Success", status=200, data=[])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/view", methods=["POST"])
def view_device_in_room():
    # print(request.json)
    room_device = RoomDevice.query.filter_by(
        id=request.json["device_id"], room_id=request.json["room_id"]
    ).first()
    print(room_device)
    if room_device is not None:
        print(room_device.room_sub_type)
        final_data = {
            "floor_id": room_device.floor_id,
            "building_id": room_device.building_id,
            "room_id": room_device.room_id,
            "device_name": room_device.name,
            "protocol_id": room_device.protocol_id,
            "device_type_id": room_device.device_type_id,
            "sub_room_type_id": room_device.room_sub_type_id,
            "sub_device_type_id": room_device.device_sub_type_id,
            "is_multiple": room_device.is_group,
            "device_group_name": room_device.group_name,
            "icon": room_device.icon,
            "add_to_home_screen": room_device.add_to_home_screen,
            "is_published": room_device.is_published,
            "remark": room_device.remark,
            "device_make": room_device.device_make,
            "device_model": room_device.device_model,
            "device_config": json.loads(room_device.device_config),
            "is_service": room_device.is_service,
            "room_sub_type": {
                "name": room_device.room_sub_type.name,
                "id": room_device.room_sub_type.id,
            },
            "device_type": {
                "name": room_device.device_type.name,
                "id": room_device.device_type.id,
            },
            "sub_room_type": {
                "name": room_device.device_sub_type.name,
                "id": room_device.device_sub_type.id,
            },
        }

        return response_base(message="Success", status=200, data=[final_data])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/edit", methods=["POST"])
def edit_device_in_room():
    print(request.json)
    device = RoomDevice.query.get_or_404(request.json["device_id"])
    if device is not None:
        print(request.json)
        device.device_type_id = request.json["device_type_id"]
        device.device_sub_type_id = request.json["sub_device_type_id"]
        device.room_sub_type_id = request.json["sub_room_type_id"]
        device.is_published = request.json["is_published"]
        device.add_to_home_screen = request.json["add_to_home_screen"]
        device.icon = request.json["icon"]
        device.remark = request.json["remark"]
        device.protocol_id = request.json["protocol_id"]
        device.name = request.json["device_name"]
        device.group_name = request.json["device_group_name"]
        device.is_group = request.json["is_multiple"]
        device.is_service = request.json["is_service"]
        device.device_make = request.json["device_make"]
        device.device_model = request.json["device_model"]
        device.device_config = json.dumps(request.json["device_config"])
        # room_number = room.number
        db.session.commit()
        return response_base(message="Success", status=200, data=[{"id": device.id}])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/list", methods=["POST"])
def list_device_in_room():
    print(request.json)
    final_data = {}
    room_device = RoomDevice.query.filter_by(room_id=request.json["room_id"]).all()
    for device in room_device:
        devicez = {}
        devicez["device_id"] = device.id
        devicez["device_name"] = device.name
        devicez["device_sub_type"] = device.device_sub_type.name
        devicez["room_sub_type"] = device.room_sub_type.name
        devicez["device_type"] = device.device_type.name
        devicez["is_published"] = device.is_published
        devicez["icon"] = device.icon
        devicez["protocol"] = device.protocol.name
        if device.device_type.technical_name not in final_data.keys():
            final_data[device.device_type.technical_name] = [devicez]
        else:
            final_data[device.device_type.technical_name].append(devicez)
    print(final_data)
    if room_device is not None:
        return response_base(message="Success", status=200, data=final_data)
    else:
        return response_base(message="Failed", status=404)
