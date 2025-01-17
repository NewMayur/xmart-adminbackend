from flask import current_app
from flask import request

from app.schema.Property import Property
from app.schema.Room import Room
from app.schema.Building import Building, Floor
from server import app
from app.extensions.db import db
from app.extensions.responses import response_base
from app.extensions.utils import get_local_ip, get_ssid
from app.schema.Room import Room, RoomDevice, RoomDeviceType, RoomRoomSubType


@app.route("/building/create", methods=["POST"])
def building():
    try:
        print(request.json)
        building = Building(
            name=request.json["name"],
            number=request.json["building_number"],
            number_of_floors=request.json["number_of_floors"],
            property_id=request.json["property_id"],
        )
        db.session.add(building)
        db.session.flush()
    except Exception as e:
        print(e)
        db.session.rollback()
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)
    for floor in request.json["floors"]:
        floor = Floor(
            name=floor["name"],
            number=floor["floor_number"],
            building_id=building.id,
            property_id=request.json["property_id"],
        )
        db.session.add(floor)
    db.session.commit()
    return response_base(
        message="Success", status=200, data={"building_id": building.id}
    )

@app.route("/building/edit", methods=["PUT"])
def edit_building():
    try:
        property_id = request.json["property_id"]
        property = Property.query.get(property_id)
        if not property:
            return response_base("Property not found", status=404)

        building_id = request.json["building_id"]
        building = Building.query.get(building_id)
        if not building:
            return response_base(message="Building not found", status=404)

        building.name = request.json.get("name", building.name)
        building.number = request.json.get("building_number", building.number)
        building.number_of_floors = request.json.get("number_of_floors", building.number_of_floors)
        db.session.commit()

        for floor_data in request.json.get("floors", []):
            floor_id = floor_data.get("id")
            if floor_id:
                floor = Floor.query.get(floor_id)
                if floor:
                    floor.name = floor_data.get("name", floor.name)
                    floor.number = floor_data.get("floor_number", floor.number)
        db.session.commit()

        return response_base(message="Building updated successfully", status=200, data={"building_id": building_id})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/building/view", methods=["POST"])
def building_view():

    building = Building.query.get_or_404(request.json["building_id"])
    if building is not None:
        print(building.name)
        print(building.floors)
        floor_data = []
        for floor in building.floors:
            floor_data.append(
                {
                    "id": floor.id,
                    "name": floor.name,
                    "floor_number": floor.number,
                }
            )
        buidling_data = {   
            "building_id": building.id,
            "name": building.name,
            "building_number": building.number,
            "number_of_floors": building.number_of_floors,
            "floors": floor_data,
            "property_id": building.property_id
        }
        return response_base(message="Success", status=200, data=[buidling_data])
    else:
        return response_base(message="Failed", status=404)



@app.route("/building/list", methods=["POST"])
def building_list():
    property_id = request.json["property_id"]
    buildings = Building.query.filter_by(property_id=property_id).all()
    final_list = []
    for building in buildings:
        data = {
            "id": building.id,
            "name": building.name,
            "number": building.number,
            "number_of_floors": building.number_of_floors,
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/building/delete", methods=["DELETE"])
def building_delete():
    building_id = request.json["building_id"]
    building = Building.query.filter_by(id=building_id).first()
    if not building:
        return response_base(message="Failed", status=404, data=[])
    else:
        for floor in building.floors:
            # floor = Floor
            for room in floor.rooms:
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
                # for device in room.room_devices:
                #     db.session.delete(device)
                # for room_sub_type in room.room_sub_types:
                #     db.session.delete(room_sub_type)
                # for room_device_type in room.room_device_types:
                #     db.session.delete(room_device_type)
                # db.session.delete(room)
            db.session.delete(floor)
        
        db.session.delete(building)
        db.session.commit()  # Commit the changes to the database
        return response_base(message="Success", status=200, data=[])

@app.route("/floor/list", methods=["POST"])
def floor_list():
    property_id = request.json["property_id"]
    building_id = request.json["building_id"]
    floors = Floor.query.filter_by(
        property_id=property_id, building_id=building_id
    ).all()
    final_list = []
    for floor in floors:
        print(floor.rooms)
        room_data = []
        for room in floor.rooms:
            print(room.__dict__)
            room_data.append(
                {
                    "id": room.id,
                    "name": room.name,
                    "number": room.number,
                    "building": room.buildings.name,
                    "room_type": room.room_type.name,
                    "sub_room_types": [subtype.name for subtype in room.room_sub_types],
                }
            )
        data = {
            "id": floor.id,
            "name": floor.name,
            "number": floor.number,
            "rooms": room_data,
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/network/info", methods=["GET"])
def network_info():
    ip, subnet_mask = get_local_ip()
    ssid = get_ssid()
    return response_base(
        message="Success",
        status=200,
        data=[{"ip": ip, "ssid": ssid, "sunet_mask": subnet_mask}],
    )

