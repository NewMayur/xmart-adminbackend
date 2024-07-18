from flask import current_app, request

from app.extensions.db import db
from app.extensions.responses import response_base
from app.schema.Building import Building, Floor
from app.schema.Room import Room, RoomDevice, RoomDeviceType, RoomRoomSubType
from app.schema.Experience import Experience, ExperienceRoomType, ExperienceDevice
from server import app
import json
import sqlalchemy.orm.exc 

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
            if "sub_room_type_ids" in room and room["sub_room_type_ids"]:
                for sub_room in room["sub_room_type_ids"]:
                    room_sub_type = RoomRoomSubType(
                        room_id=room_new.id,
                        room_sub_type_id=sub_room,
                        floor_id=room["floor_id"],
                        building_id=room["building_id"],
                        property_id=room["property_id"],
                    )
                    db.session.add(room_sub_type)

            for device in room["device_types"]:
                room_device_type = RoomDeviceType(
                    room_id=room_new.id,
                    device_type_id=device,
                    floor_id=room["floor_id"],
                    building_id=room["building_id"],
                    property_id=room["property_id"],
                )
                db.session.add(room_device_type)
            
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
    floor = Floor.query.filter_by(id = request.json["floor_id"]).first()
    if floor is None:
        return response_base(message="Failed", status=404, data=[])
    else:
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


# Pagination
@app.route("/floor/room/v1/list", methods=["POST"])
def get_room_v1():
    page = int(request.json.get("page", 1))
    per_page = int(request.json.get("per_page", 5))

    if page <= 0 :
        page = 1
    if per_page <= 0:
        per_page = 5
    
    floor = Floor.query.get_or_404(request.json["floor_id"])
    rooms = Room.query.filter_by(floor_id = floor.id).paginate(page=page,  per_page=per_page)
    final_data = []
    for room in rooms:
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


# Pagination with Parameters
@app.route("/floor/room/v1/list_with_param", methods=["POST"])
def get_room_with_param_v1(page: int = 1, per_page: int = 5, room_name: str = None):
    floor = Floor.query.get_or_404(request.json["floor_id"])
    rooms_query = Room.query.filter_by(floor_id=floor.id)

    if room_name:
        rooms_query = rooms_query.filter(Room.name == room_name)

    rooms = rooms_query.paginate(page=page, per_page=per_page)
    final_data = []
    for room in rooms:
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
    print(request.json)
    room = Room.query.filter_by(id=request.json["room_id"]).first()
    # print(room)
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


@app.route("/roomsubroom/list", methods=["POST"])
def view_room_sub_room():
    print(request.json)
    room = Room.query.filter_by(id=request.json["room_id"]).first()
    # print(room)
    if room is not None:
        subroom = [
            {"name": subtype.name, "id": subtype.id} for subtype in room.room_sub_types
        ]
        return response_base(message="Success", status=200, data=subroom)
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


@app.route("/room/edit", methods=['PUT'])
def edit_room():
    data = request.json
    room_id = data.get('room_id')

    room = Room.query.get(room_id)

    if room:
        # Update room details
        room.name = data.get('name')
        room.number = data.get('number')
        room.room_type_id = data.get('room_type_id')
        room.floor_id = data.get('floor_id')

        # Add or remove devices
        for device_id in data.get('device_type_new', []):
            room_device_type = RoomDeviceType(
                room_id=room.id, 
                device_type_id=device_id, 
                floor_id=room.floor_id, 
                building_id=room.building_id, 
                property_id=room.property_id
            )
            db.session.add(room_device_type)

        for device_id in data.get('device_type_old', []):
            room_device_type = RoomDeviceType.query.filter_by(room_id=room.id, device_type_id=device_id).first()
            if room_device_type:
                db.session.delete(room_device_type)

        # Add or remove subrooms
        for subroom_id in data.get('sub_room_type_new', []):
            room_sub_type = RoomRoomSubType(
                room_id=room.id, 
                room_sub_type_id=subroom_id,
                floor_id=room.floor_id,
                building_id=room.building_id,
                property_id=room.property_id
            )
            db.session.add(room_sub_type)

        for subroom_id in data.get('sub_room_type_old', []):
            room_sub_type = RoomRoomSubType.query.filter_by(room_id=room.id, room_sub_type_id=subroom_id).first()
            if room_sub_type:
                db.session.delete(room_sub_type)

        db.session.commit()
        return response_base(message="Success", status=200, data=[])
    else:
        return response_base(message="Room not found", status=404, data=[])


@app.route("/room/device/add", methods=["POST"])
def add_device_to_room():
    room = Room.query.filter_by(id=request.json["room_id"]).first()
    if room is not None:
        if request.json["device_type_id"] == 5:  # TV device type
            # Check how many remotes the TV already has
            remotes_count = RoomDevice.query.filter_by(
                room_id=room.id,
                device_type_id=5,  # TV
            ).count()

            if remotes_count >= 2:
                return response_base(message="TV can have only two remotes", status=400, data=[])

            # Check for specific remote types
            if request.json["sub_device_type_id"] == 17:  # IR TV remote
                existing_ir_tv_remote = RoomDevice.query.filter_by(
                    room_id=room.id,
                    device_type_id=5,
                    device_sub_type_id=17
                ).first()
                if existing_ir_tv_remote:
                    return response_base(message="Already an IR TV remote exists", status=400, data=[])
            elif request.json["sub_device_type_id"] == 18:  # IR STB remote
                existing_ir_stb_remote = RoomDevice.query.filter_by(
                    room_id=room.id,
                    device_type_id=5,
                    device_sub_type_id=18
                ).first()
                if existing_ir_stb_remote:
                    return response_base(message="Already an IR STB remote exists", status=400, data=[])

        # Proceed with adding the device
        room_device = RoomDevice(
            room_id=room.id,
            floor_id=request.json["floor_id"],
            building_id=request.json["building_id"],
            property_id=request.json["property_id"],
            device_type_id=request.json["device_type_id"],
            device_sub_type_id=request.json["sub_device_type_id"],
            room_sub_type_id=(
                request.json["sub_room_type_id"]
                if request.json["sub_room_type_id"] not in ["0", 0, None]
                else None
            ),
            is_published=request.json["is_published"],
            add_to_home_screen=request.json["add_to_home_screen"],
            icon=request.json["icon"],
            remark=request.json["remark"],
            protocol_id=request.json["protocol_id"],
            name=request.json["device_name"],
            group_name=request.json["device_group_name"],
            is_group=request.json["is_multiple"],
            is_service=1 if request.json["sub_device_type_id"] == 5 else 0,
            device_meta=json.dumps(request.json["device_meta"]),
            device_config=json.dumps(request.json["device_config"]),
            room_number=room.number,
        )
        db.session.add(room_device)
        db.session.commit()
        return response_base(message="Success", status=200, data=[{"id": room_device.id}])
    else:
        return response_base(message="Failed", status=404, data=[])

@app.route("/room/device/delete", methods=["DELETE"])
def delete_device_from_room():
    # print(request.json)
    for device_id in request.json["device_ids"]:
        room_device = RoomDevice.query.filter_by(
            id=device_id, room_id=request.json["room_id"]
        ).first()
        if room_device is not None:
            db.session.delete(room_device)
            db.session.commit()

        else:
            pass
            # return response_base(message="Failed", status=404)
    return response_base(message="Success", status=200, data=[])


@app.route("/room/device/view", methods=["POST"])
def view_device_in_room():
    # print(request.json)
    room_device = RoomDevice.query.filter_by(
        id=request.json["device_id"], room_id=request.json["room_id"]
    ).first()
    # print(room_device.protocol)
    if room_device is not None:
        print(room_device.room_sub_type)
        final_data = {
            "floor_id": room_device.floor_id,
            "building_id": room_device.building_id,
            "room_id": room_device.room_id,
            "device_name": room_device.name,
            "protocol_id": room_device.protocol_id,
            "device_type_id": room_device.device_type_id,
            "sub_room_type_id": room_device.room_sub_type.id if room_device.room_sub_type is not None else 0,
            "sub_device_type_id": room_device.device_sub_type_id,
            "is_multiple": room_device.is_group,
            "device_group_name": room_device.group_name,
            "icon": room_device.icon,
            "add_to_home_screen": room_device.add_to_home_screen,
            "is_published": room_device.is_published,
            "remark": room_device.remark,
            "device_config": json.loads(room_device.device_config),
            "device_meta": json.loads(room_device.device_meta),
            "is_service": room_device.is_service,
            "room_sub_type": (
                {
                    "name": room_device.room_sub_type.name if room_device.room_sub_type is not None else "",
                    "id": room_device.room_sub_type.id if room_device.room_sub_type is not None else 0,
                }
            ),
            "device_type": {
                "name": room_device.device_type.name,
                "id": room_device.device_type.id,
            },
            "sub_device_type": {
                "name": room_device.device_sub_type.name,
                "id": room_device.device_sub_type.id,
            },
            "protocol": {
                "id": room_device.protocol.id,
                "name": room_device.protocol.name,
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
        device.device_config = json.dumps(request.json["device_config"])
        device.device_meta = json.dumps(request.json["device_meta"])
        # room_number = room.number
        db.session.commit()
        return response_base(message="Success", status=200, data=[{"id": device.id}])
    else:
        return response_base(message="Failed", status=404)


@app.route("/room/device/list", methods=["POST"])
def list_device_in_room():
    print(request.json)
    final_data = []
    room_device = RoomDevice.query.filter_by(
        room_id=request.json["room_id"], device_type_id=request.json["device_type_id"]
    ).all()
    for device in room_device:
        final_data.append(
            {
                "device_id": device.id,
                "device_name": device.name,
                "device_sub_type": device.device_sub_type.name,
                "room_sub_type": device.room_sub_type.name if device.room_sub_type is not None else "",
                "device_type": device.device_type.name,
                "is_published": device.is_published,
                "icon": device.icon,
                "protocol": device.protocol.name,
                "is_service": device.is_service,
            }
        )
    if room_device is not None:
        return response_base(message="Success", status=200, data=final_data)
    else:
        return response_base(message="Failed", status=404)



@app.route("/room/delete", methods=["DELETE"])
def delete_room():
    room_ids = request.json.get("room_ids", [])
    if not room_ids:
        return response_base(message="No room IDs provided", status=400, data=[])

    try:
        rooms = Room.query.filter(Room.id.in_(room_ids)).all()

        for room in rooms:
            if room is not None:
                # Delete sub rooms
                sub_rooms = RoomRoomSubType.query.filter_by(room_id=room.id).all()
                for sub_room in sub_rooms:
                    db.session.delete(sub_room)

                # Delete room devices
                room_devices = RoomDevice.query.filter_by(room_id=room.id).all()
                for dev in room_devices:
                    db.session.delete(dev)

                # Delete room device types
                room_device_types = RoomDeviceType.query.filter_by(room_id=room.id).all()
                for room_device_type in room_device_types:
                    db.session.delete(room_device_type)
                db.session.flush()
                # Delete the room itself
            db.session.delete(room)

        db.session.commit()
        return response_base(message="Success", status=200, data=[])

    except sqlalchemy.orm.exc.StaleDataError as e:
        db.session.rollback()
        return response_base(message="Stale data error occurred", status=500, data=str(e))

    except Exception as e:
        db.session.rollback()
        return response_base(message="An error occurred", status=500, data=str(e))


@app.route("/roomdeviceunique/list", methods=["GET"])
def room_device_unique():
    # print(request.json)
    rooms = Room.query.filter_by(room_type_id=request.json["room_type_id"]).all()
    device_type_staging = []
    for room in rooms:
        device_type_staging.append(room.device_type_id)

    return response_base(message="Success", status=200, data=[])
