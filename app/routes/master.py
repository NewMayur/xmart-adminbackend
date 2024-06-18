from flask import request, jsonify, send_file
from server import app
from app.schema.User import User
from app.schema.Master import (
    MasterRoomType,
    MasterSubRoomType,
    MasterDeviceType,
    MasterDeviceSubType,
    MasterProtocol,
)
from app.schema.Property import MasterPropertyType
from app.extensions.db import db
from app.extensions.responses import response_base
from app.seeder.seed import seed
from app.schema.Device import KnxDeviceSubTypeData, BacNetDeviceSubTypeData
import os
import pandas as pd


@app.route("/master/roomtype/list", methods=["GET"])
def room_type_master_fetch():
    room_types = MasterRoomType.query.all()
    final_list = []
    for room_type in room_types:
        data = {
            "id": room_type.id,
            "name": room_type.name,
            "technical_name": room_type.technical_name,
        }
        final_list.append(data)
    return response_base(message="Success", status=200, data=final_list)


@app.route("/master/subroomtype/list", methods=["GET"])
def subroom_type_fetch():
    sub_room_types = MasterSubRoomType.query.all()
    final_list = []
    for sub_room_type in sub_room_types:
        data = {
            "id": sub_room_type.id,
            "name": sub_room_type.name,
            "technical_name": sub_room_type.technical_name,
        }
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
    if request.json["protocol_id"] == 2:
        data = KnxDeviceSubTypeData.query.filter_by(
            device_type_id=request.json["device_type_id"],
            sub_device_type_id=request.json["device_sub_type_id"],
        ).all()
        print(data)
        for dat in data:
            final_list.append(
                {
                    "id": dat.id,
                    "name": dat.address_name,
                    "technical_name": dat.address_name_technical,
                    "value_data_type": dat.value_data_type,
                    "value_data_range": dat.value_data_range,
                }
            )
    else:
        data = BacNetDeviceSubTypeData.query.filter_by(
            device_type_id=request.json["device_type_id"],
            sub_device_type_id=request.json["device_sub_type_id"],
        )
        for dat in data:
            final_list.append(
                {
                    "id": dat.id,
                    "function": dat.function,
                    "object_instance": dat.object_instance,
                    "object_type": dat.object_type,
                    "range": dat.range,
                    "read_write": dat.read_write,
                    "technical_name": dat.technical_name,
                }
            )
    return response_base(message="Success", status=200, data=final_list)


@app.route("/health", methods=["GET"])
def heatlh_check():

    return response_base(message="Connected to server.", status=200, data=[])


@app.route("/uploadmaster", methods=["POST"])
def upload_master():
    # print(request.files)
    try:
        request.files["file"].save(
            os.path.join("static", request.files["file"].filename)
        )
        file_path = os.path.join("static", request.files["file"].filename)
        if os.path.isfile(file_path):
            df = pd.read_excel(file_path)
            print(df)
            if request.form["type"] == "property":
                for row in df.iloc:
                    property = MasterPropertyType.query.filter_by(
                        technical_name=row["technical_name"], name=row["name"]
                    ).first()
                    if property is None:
                        new_property = MasterPropertyType(
                            name=row["name"],
                            technical_name=row["technical_name"],
                        )
                        db.session.add(new_property)
                    else:
                        pass
                db.session.commit()
            if request.form["type"] == "room":
                for row in df.iloc:
                    room = MasterRoomType.query.filter_by(
                        technical_name=row["technical_name"], name=row["name"]
                    ).first()
                    if room is None:
                        new_room = MasterRoomType(
                            name=row["name"],
                            technical_name=row["technical_name"],
                        )
                        db.session.add(new_room)
                    else:
                        pass
                db.session.commit()
            if request.form["type"] == "sub_room":
                for row in df.iloc:
                    sub_room = MasterSubRoomType.query.filter_by(
                        technical_name=row["technical_name"], name=row["name"]
                    ).first()
                    if sub_room is None:
                        sub_room_new = MasterSubRoomType(
                            name=row["name"],
                            technical_name=row["technical_name"],
                        )
                        db.session.add(sub_room_new)
                    else:
                        pass
                db.session.commit()
            elif request.form["type"] == "device":
                for row in df.iloc:
                    device = MasterDeviceType.query.filter_by(
                        technical_name=row["device_name_technical"],
                        name=row["device_name"],
                    ).first()
                    if device is None:
                        new_device = MasterDeviceType(
                            name=row["device_name"],
                            technical_name=row["device_name_technical"],
                        )
                        db.session.add(new_device)
                        db.session.flush()
                        sub_device_type = MasterDeviceSubType(
                            name=row["subtype_name"],
                            technical_name=row["subtype_name_technical"],
                            master_device_type_id=new_device.id,
                        )
                        db.session.add(new_device)
                        db.session.add(sub_device_type)
                    else:
                        device_sub_type = MasterDeviceSubType.query.filter_by(
                            name=row["subtype_name"],
                            technical_name=row["subtype_name_technical"],
                            master_device_type_id=device.id,
                        ).first()
                        if device_sub_type is None:
                            sub_device_type = MasterDeviceSubType(
                                name=row["subtype_name"],
                                technical_name=row["subtype_name_technical"],
                                master_device_type_id=device.id,
                            )
                            db.session.add(sub_device_type)
                        else:
                            pass
            elif request.form["type"] == "knx":
                device_sub_device = MasterDeviceSubType.query.all()
                device_sub_device_dat = {}
                for sub_d in device_sub_device:
                    device_sub_device_dat[
                        sub_d.technical_name
                        + "#"
                        + sub_d.master_device_type_new.technical_name
                    ] = (str(sub_d.id) + "#" + str(sub_d.master_device_type_new.id))
                    # print(sub_d.master_device_type_new.id)
                print(device_sub_device_dat)
                # exit()
                for row in df.iloc:
                    print(row)
                    sub_dev, dev_id = device_sub_device_dat[
                        row["subdevice_name_technical"]
                        + "#"
                        + row["device_name_technical"]
                    ].split("#")
                    print(sub_dev, dev_id)
                    device = KnxDeviceSubTypeData.query.filter_by(
                        device_type_id=dev_id,
                        sub_device_type_id=sub_dev,
                        address_name_technical=row["address_name_technical"],
                        address_name=row["address_name"],
                        value_data_type=row["value_data_type"],
                        value_data_range=row["value_data_range"],
                    ).first()
                    if device is None:
                        new_device = KnxDeviceSubTypeData(
                            device_type_id=dev_id,
                            sub_device_type_id=sub_dev,
                            address_name=row["address_name"],
                            address_name_technical=row["address_name_technical"],
                            value_data_type=row["value_data_type"],
                            value_data_range=row["value_data_range"],
                        )
                        db.session.add(new_device)
                    else:
                        pass
            elif request.form["type"] == "bacnet":
                for row in df.iloc:
                    device = BacNetDeviceSubTypeData.query.filter_by(
                        device_type_id=dev_id,
                        sub_device_type_id=sub_dev,
                        function=row["function"],
                        object_instance=row["object_instance"],
                        object_type=row["object_type"],
                        range=row["range"],
                        read_write=row["read_write"],
                    ).first()
                    if device is None:
                        new_device = BacNetDeviceSubTypeData(
                            device_type_id=dev_id,
                            sub_device_type_id=sub_dev,
                            function=row["function"],
                            object_instance=row["object_instance"],
                            object_type=row["object_type"],
                            range=row["range"],
                            read_write=row["read_write"],
                        )
                        db.session.add(new_device)
            db.session.commit()
            return response_base(message="Success", status=200)
        else:
            return response_base(message="Something went wrong", status=500)
        return response_base(message="Success", status=200)
    except Exception as e:
        print(e)
        return response_base(message="Failed", status=500)


@app.route("/downloadmasters", methods=["GET"])
def download_master():
    master = request.args.get("master")
    print(master)
    return send_file(f"master/master_{master}.xlsx", as_attachment=True)


@app.route("/master/propertytype", methods=["GET"])
def property_type_master():
    data = MasterPropertyType.query.all()
    final_data = []
    for dat in data:
        final_data.append({"id": dat.id, "name": dat.name})
    return response_base(message="Success", status=200, data=final_data)
