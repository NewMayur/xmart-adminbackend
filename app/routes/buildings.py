from flask import current_app
from flask import request
from server import app
from app.schema.Building import Building, Floor
from app.extensions.db import db
from app.extensions.responses import response_base


@app.route("/building/create", methods=["POST"])
def building():
    try:
        building = Building(
            name=request.json["name"],
            number=request.json["building_number"],
            number_of_floors=request.json["number_of_floors"],
            property_id=request.json["property_id"],
        )
        db.session.add(building)
        db.session.flush()
    except Exception as e:
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
                    "number": floor.number,
                }
            )
        buidling_data = {
            "building_id": building.id,
            "name": building.name,
            "number": building.number,
            "number_of_floors": building.number_of_floors,
            "floors": floor_data,
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
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


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
