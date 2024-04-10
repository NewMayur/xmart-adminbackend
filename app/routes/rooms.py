from app.schema.Room import Room, RoomRoomSubType, RoomDeviceType
from app.schema.Building import Building, Floor
from flask import request, current_app
from app.extensions.db import db
from app.extensions.responses import response_base
from server import app

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
