from flask import request, jsonify
from server import app
from app.schema.User import User
from app.schema.Master import MasterRoomType, MasterSubRoomType, MasterDeviceType
from app.extensions.db import db
from app.extensions.responses import response_base


@app.route("/master/roomtype/list", methods=["GET"])
def room_type_master_fetch():
    room_types = MasterRoomType.query.all()
    final_list = []
    for room_type in room_types:
        data = {"id": room_type.id, "name": room_type.name}
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/subroomtype/list", methods=["GET"])
def subroom_type_fetch():
    sub_room_types = MasterSubRoomType.query.all()
    final_list = []
    for sub_room_type in sub_room_types:
        data = {"id": sub_room_type.id, "name": sub_room_type.name}
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/devicetype/list", methods=["GET"])
def device_type_fetch():
    device_types = MasterDeviceType.query.all()
    final_list = []
    for device_type in device_types:
        data = {"id": device_type.id, "name": device_type.name}
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)
