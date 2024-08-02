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
from app.schema.Room import RoomDevice
import os
#import pandas as pd
import json

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


import json

@app.route("/master/add_test_device", methods=["POST"])
def add_test_device():
    try:
        data = request.json
        print(f"Received data: {data}")

        # Extract device type information
        device_type_info = data.get("device_type")
        device_type_name = device_type_info.get("name")
        device_type_technical_name = device_type_info.get("technical_name")
        experience_config = json.dumps(device_type_info.get("experience_config", '{}'))

        # Extract subtypes information
        subtypes = data.get("subtypes", [])

        # Check if the device type already exists
        device_type = MasterDeviceType.query.filter_by(technical_name=device_type_technical_name).first()
        if device_type:
            # Remove existing sub-device types and their fields
            existing_subtypes = MasterDeviceSubType.query.filter_by(master_device_type_id=device_type.id).all()
            for subtype in existing_subtypes:
                KnxDeviceSubTypeData.query.filter_by(sub_device_type_id=subtype.id).delete()
                BacNetDeviceSubTypeData.query.filter_by(sub_device_type_id=subtype.id).delete()
                db.session.delete(subtype)
            db.session.flush()
        else:
            # Create the new device type
            device_type = MasterDeviceType(
                name=device_type_name,
                technical_name=device_type_technical_name,
                experience_config=experience_config  # Provide the experience config
            )
            db.session.add(device_type)
            db.session.flush()  # Ensure the new device type ID is available

        # Add the new sub-device types
        for subtype in subtypes:
            new_subtype = MasterDeviceSubType(
                name=subtype["name"],
                technical_name=subtype["technical_name"],
                master_device_type_id=device_type.id,
            )
            db.session.add(new_subtype)
            db.session.flush()  # Ensure the new subtype ID is available

            # Check for KNX and BACnet data
            knx_data_list = subtype.get("knx_data")
            bacnet_data_list = subtype.get("bacnet_data")

            if knx_data_list and bacnet_data_list:
                return response_base(message="Device can't have both protocols", status=400, data=[])

            # Add KNX data
            if knx_data_list:
                for knx_entry_data in knx_data_list:
                    knx_entry = KnxDeviceSubTypeData(
                        device_type_id=device_type.id,
                        sub_device_type_id=new_subtype.id,
                        address_name_technical=knx_entry_data["address_name_technical"],
                        address_name=knx_entry_data["address_name"],
                        value_data_type=knx_entry_data["value_data_type"],
                        value_data_range=knx_entry_data["value_data_range"],
                    )
                    db.session.add(knx_entry)

            # Add BACnet data
            if bacnet_data_list:
                for bacnet_data in bacnet_data_list:
                    bacnet_entry = BacNetDeviceSubTypeData(
                        device_type_id=device_type.id,
                        sub_device_type_id=new_subtype.id,
                        technical_name=bacnet_data["technical_name"],
                        function=bacnet_data["function"],
                        object_instance=bacnet_data["object_instance"],
                        object_type=bacnet_data["object_type"],
                        range=bacnet_data["range"],
                        read_write=bacnet_data["read_write"],
                    )
                    db.session.add(bacnet_entry)

        db.session.commit()
        return response_base(message="Test device and sub-device added successfully", status=200, data=[])
    except Exception as e:
        db.session.rollback()
        return response_base(message=str(e), status=500, data=[])


@app.route("/master/delete_device_type", methods=["POST"])
def delete_device_type():
    try:
        device_type_id = request.json.get("device_type_id")
        if not device_type_id:
            return response_base(message="Device type ID is required", status=400, data=[])

        # Fetch the device type
        device_type = MasterDeviceType.query.get(device_type_id)
        if not device_type:
            return response_base(message="Device type not found", status=404, data=[])

        # Fetch and delete all sub-device types and their fields
        sub_device_types = MasterDeviceSubType.query.filter_by(master_device_type_id=device_type_id).all()
        for subtype in sub_device_types:
            KnxDeviceSubTypeData.query.filter_by(sub_device_type_id=subtype.id).delete()
            BacNetDeviceSubTypeData.query.filter_by(sub_device_type_id=subtype.id).delete()
            db.session.delete(subtype)

        # Delete the master device type
        db.session.delete(device_type)
        db.session.commit()

        return response_base(message="Device type and its sub-device types deleted successfully", status=200, data=[])
    except Exception as e:
        db.session.rollback()
        return response_base(message=str(e), status=500, data=[])

  
@app.route("/master/delete_sub_device_type", methods=["DELETE"])
def delete_sub_device_type():
    try:
        data = request.json

        # Extract device type ID and sub-device type ID
        device_type_id = data.get("device_type_id")
        sub_device_type_id = data.get("sub_device_type_id")

        if not device_type_id or not sub_device_type_id:
            return response_base(message="Device type ID and sub-device type ID are required", status=400, data=[])

        # Fetch the sub-device type
        sub_device_type = MasterDeviceSubType.query.filter_by(
            id=sub_device_type_id, master_device_type_id=device_type_id
        ).first()

        if not sub_device_type:
            return response_base(message="Sub-device type not found", status=404, data=[])

        # Delete associated KNX data
        knx_data = KnxDeviceSubTypeData.query.filter_by(
            device_type_id=device_type_id, sub_device_type_id=sub_device_type_id
        ).all()
        for knx_entry in knx_data:
            db.session.delete(knx_entry)

        # Delete associated BACnet data
        bacnet_data = BacNetDeviceSubTypeData.query.filter_by(
            device_type_id=device_type_id, sub_device_type_id=sub_device_type_id
        ).all()
        for bacnet_entry in bacnet_data:
            db.session.delete(bacnet_entry)

        # Delete RoomDevice entries that reference the sub-device type
        room_devices = RoomDevice.query.filter_by(device_sub_type_id=sub_device_type_id).all()
        for room_device in room_devices:
            db.session.delete(room_device)

        # Delete the sub-device type
        db.session.delete(sub_device_type)
        db.session.commit()

        return response_base(message="Sub-device type and associated fields deleted successfully", status=200, data=[])
    except Exception as e:
        db.session.rollback()
        return response_base(message=str(e), status=500, data=[])
@app.route("/master/update_device_type", methods=["POST"])
def update_device_type():
    try:
        data = request.json
        print(f"Received data: {data}")

        # Extract device type information
        device_type_id = data.get("device_type_id")
        device_type_info = data.get("device_type")
        subtypes = data.get("subtypes", [])

        if not device_type_id or not device_type_info:
            return response_base(message="Device type ID and information are required", status=400, data=[])

        # Fetch the existing device type
        device_type = MasterDeviceType.query.get(device_type_id)
        if not device_type:
            return response_base(message="Device type not found", status=404, data=[])

        # Update device type information
        device_type.name = device_type_info.get("name", device_type.name)
        device_type.technical_name = device_type_info.get("technical_name", device_type.technical_name)
        device_type.experience_config = json.dumps(device_type_info.get("experience_config", device_type.experience_config))

        # Update or add sub-device types
        existing_subtypes = {subtype.id: subtype for subtype in MasterDeviceSubType.query.filter_by(master_device_type_id=device_type_id).all()}
        for subtype_data in subtypes:
            print(f"Processing subtype_data: {subtype_data}")

            subtype_id = subtype_data.get("id")
            if subtype_id and subtype_id in existing_subtypes:
                # Update existing sub-device type
                subtype = existing_subtypes[subtype_id]
                subtype.name = subtype_data.get("name", subtype.name)
                subtype.technical_name = subtype_data.get("technical_name", subtype.technical_name)
            else:
                # Add new sub-device type
                new_subtype = MasterDeviceSubType(
                    name=subtype_data["name"],
                    technical_name=subtype_data["technical_name"],
                    master_device_type_id=device_type.id,
                )
                db.session.add(new_subtype)
                db.session.flush()  # Ensure the new subtype ID is available
                subtype = new_subtype  # Assign to subtype for later use

            # Check for KNX and BACnet data
            knx_data_list = subtype_data.get("knx_data", [])
            bacnet_data_list = subtype_data.get("bacnet_data", [])

            if knx_data_list and bacnet_data_list:
                return response_base(message="Device can't have both protocols", status=400, data=[])

            if knx_data_list:
                for knx_data in knx_data_list:
                    print(f"Processing KNX data: {knx_data}")
                    knx_entry = KnxDeviceSubTypeData.query.filter_by(
                        device_type_id=device_type.id,
                        sub_device_type_id=subtype.id,
                        address_name_technical=knx_data["address_name_technical"]
                    ).first()
                    if knx_entry:
                        knx_entry.address_name = knx_data.get("address_name", knx_entry.address_name)
                        knx_entry.value_data_type = knx_data.get("value_data_type", knx_entry.value_data_type)
                        knx_entry.value_data_range = knx_data.get("value_data_range", knx_entry.value_data_range)
                    else:
                        knx_entry = KnxDeviceSubTypeData(
                            device_type_id=device_type.id,
                            sub_device_type_id=subtype.id,
                            address_name_technical=knx_data["address_name_technical"],
                            address_name=knx_data["address_name"],
                            value_data_type=knx_data["value_data_type"],
                            value_data_range=knx_data["value_data_range"],
                        )
                        db.session.add(knx_entry)

            if bacnet_data_list:
                for bacnet_data in bacnet_data_list:
                    print(f"Processing BACnet data: {bacnet_data}")
                    bacnet_entry = BacNetDeviceSubTypeData.query.filter_by(
                        device_type_id=device_type.id,
                        sub_device_type_id=subtype.id,
                        technical_name=bacnet_data["technical_name"]
                    ).first()
                    if bacnet_entry:
                        bacnet_entry.function = bacnet_data.get("function", bacnet_entry.function)
                        bacnet_entry.object_instance = bacnet_data.get("object_instance", bacnet_entry.object_instance)
                        bacnet_entry.object_type = bacnet_data.get("object_type", bacnet_entry.object_type)
                        bacnet_entry.range = bacnet_data.get("range", bacnet_entry.range)
                        bacnet_entry.read_write = bacnet_data.get("read_write", bacnet_entry.read_write)
                    else:
                        bacnet_entry = BacNetDeviceSubTypeData(
                            device_type_id=device_type.id,
                            sub_device_type_id=subtype.id,
                            technical_name=bacnet_data["technical_name"],
                            function=bacnet_data["function"],
                            object_instance=bacnet_data["object_instance"],
                            object_type=bacnet_data["object_type"],
                            range=bacnet_data["range"],
                            read_write=bacnet_data["read_write"],
                        )
                        db.session.add(bacnet_entry)

        db.session.commit()
        return response_base(message="Device type and sub-device types updated successfully", status=200, data=[])
    except Exception as e:
        db.session.rollback()
        return response_base(message=str(e), status=500, data=[])




