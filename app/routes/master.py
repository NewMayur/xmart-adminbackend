from flask import request, jsonify
from server import app
from app.schema.User import User
from app.schema.Master import (
    MasterRoomType,
    MasterSubRoomType,
    MasterDeviceType,
    MasterDeviceSubType,
    MasterProtocol,
)
from app.extensions.db import db
from app.extensions.responses import response_base
from app.seeder.seed import seed
from app.schema.Device import KnxDeviceSubTypeData


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
        data = {
            "id": device_type.id,
            "name": device_type.name,
            "technical_name": device_type.technical_name,
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/devicesubtype/list", methods=["GET"])
def device_sub_type_fetch():
    device_sub_types = MasterDeviceSubType.query.all()
    final_list = []
    for device_sub_type in device_sub_types:
        data = {
            "id": device_sub_type.id,
            "name": device_sub_type.name,
            "technical_name": device_sub_type.technical_name,
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/_seed", methods=["GET"])
def seed_db():
    print("datata")
    # import pandas as pd

    # data = pd.read_excel(file_path)
    seed()
    return response_base(message="Success", status=200, data=[])


@app.route("/master/devicesubdevicetype/list", methods=["GET"])
def device_sub_types():
    device_type = MasterDeviceType.query.all()
    final_list = []
    for device in device_type:
        device_data = {}
        device_data["name"] = device.name
        device_data["technical_name"] = device.technical_name
        device_data["device_sub_type"] = [
            sub_dev.name for sub_dev in device.device_sub_type_1
        ]
        print(device.device_sub_type_1)
        final_list.append(device_data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/subdevicetypeperdevietype/list", methods=["POST"])
def device_sub_types_per_device_type():
    device_sub_type = MasterDeviceSubType.query.filter_by(
        master_device_type_id=request.json["device_type_id"]
    ).all()
    final_list = []
    for device in device_sub_type:
        device_data = {}
        device_data["name"] = device.name
        device_data["technical_name"] = device.technical_name
        device_data["id"] = device.id
        # print(device.device_sub_type_1)
        final_list.append(device_data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/protocol/list", methods=["GET"])
def master_protocol_list():
    protocols = MasterProtocol.query.all()
    final_list = []
    for protocol in protocols:
        proto_data = {}
        proto_data["name"] = protocol.name
        proto_data["id"] = protocol.id
        # device_data["id"] = device.id
        # print(device.device_sub_type_1)
        final_list.append(proto_data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/subdevicedata", methods=["POST"])
def device_sub_data():
    final_list = []
    if request.json["protocol_id"] == 1:
        data = KnxDeviceSubTypeData.query.filter_by(
            device_type_id=request.json["device_type_id"],
            sub_device_type_id=request.json["device_sub_type_id"],
        ).all()
        for dat in data:
            final_list.append(
                {
                    "id": dat.id,
                    "name": dat.address_name,
                    "technical_name": dat.address_name_technical,
                    "value_data_type": dat.value_data_type,
                    "vale_data_range": dat.vale_data_range,
                }
            )
    else:
        pass
    return response_base(message="Success", status=200, data=final_list)
