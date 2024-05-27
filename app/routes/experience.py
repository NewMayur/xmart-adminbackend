from flask import current_app, request

from app.extensions.db import db
from app.extensions.responses import response_base
from app.schema.Experience import Experience, ExperienceRoomType, ExperienceDevice
from app.schema.Room import Room
from server import app
import json


@app.route("/experience/create", methods=["POST"])
def experience():
    try:
        experience = Experience(
            name=request.json["name"],
            description=request.json["description"],
            icon=request.json["icon"],
            add_to_home_screen=request.json["add_to_home_screen"],
            is_published=request.json["is_published"],
            experience_config=json.dumps(request.json["experience_config"]),
        )
        db.session.add(experience)
        db.session.flush()
        for roomtype in request.json["room_types"]:
            roomtype = ExperienceRoomType(
                experience_id=experience.id,
                room_type_id=roomtype,
            )
            db.session.add(roomtype)
        for device in request.json["devices"]:
            device = ExperienceDevice(
                experience_id=experience.id,
                device_type_id=device,
            )
            db.session.add(device)
        db.session.commit()
        return response_base(
            message="Success", status=200, data={"experience_id": experience.id}
        )
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/experience/list", methods=["GET"])
def list_experience():
    try:
        experiences = Experience.query.all()
        final_data = []
        for experience in experiences:
            final_data.append(
                {
                    "id": experience.id,
                    "name": experience.name,
                    "icon": experience.icon,
                    "is_published": experience.is_published,
                    "experience_config": json.loads(experience.experience_config),
                    "description": experience.description,
                    "devices": [
                        {"id": device.id, "name": device.name}
                        for device in experience.exp_room_device_types
                    ],
                    "room_types": [
                        {"id": room_type.id, "name": room_type.name}
                        for room_type in experience.exp_room_types
                    ],
                }
            )
            print(experience.exp_room_types)
        return response_base(message="Success", status=200, data=final_data)
    except Exception as e:
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/experience/update", methods=["POST"])
def update_experience():
    try:
        experience = Experience.query.filter_by(
            id=request.json["experience_id"]
        ).first()
        if experience is not None:
            experience.name = request.json["name"]
            experience.description = request.json["description"]
            experience.icon = request.json["icon"]
            experience.add_to_home_screen = request.json["add_to_home_screen"]
            experience.is_published = request.json["is_published"]
            experience.experience_config = json.dumps(request.json["experience_config"])
            new_entries_devices = []
            old_entries_devices = []
            new_entries_room = []
            old_entries_room = []
            for dev in request.json["devices_new"]:
                if dev not in request.json["devices_old"]:
                    new_entries_devices.append(dev)
                else:
                    pass
            for dev in request.json["devices_old"]:
                if dev not in request.json["devices_new"]:
                    old_entries_devices.append(dev)
                else:
                    pass
            for dev in request.json["room_types_new"]:
                if dev not in request.json["room_types_old"]:
                    new_entries_room.append(dev)
                else:
                    pass
            for dev in request.json["room_types_old"]:
                if dev not in request.json["room_types_new"]:
                    old_entries_room.append(dev)
                else:
                    pass
            print(new_entries_room)
            print(old_entries_room)
            # update device types
            for device in new_entries_devices:
                room_device_type = ExperienceDevice(
                    experience_id=experience.id, device_type_id=device
                )
                db.session.add(room_device_type)
            for device in old_entries_devices:
                room_device_type = ExperienceDevice.query.filter_by(
                    experience_id=experience.id, device_type_id=device
                ).first()
                db.session.delete(room_device_type)
            # Update subroom types
            for subroom in new_entries_room:
                room_sub_type = ExperienceRoomType(
                    experience_id=experience.id, room_type_id=subroom
                )
                db.session.add(room_sub_type)
            for subroom in old_entries_room:
                room_sub_type = ExperienceRoomType.query.filter_by(
                    experience_id=experience.id, room_type_id=subroom
                ).first()
                db.session.delete(room_sub_type)
            db.session.commit()
            return response_base(message="Success", status=200)
        else:
            return response_base(message="Failed", status=404)
    except Exception as e:
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/experience/delete", methods=["DELETE"])
def delete_experience():
    try:
        experience = Experience.query.filter_by(
            id=request.json["experience_id"]
        ).first()
        if experience is not None:
            db.session.delete(experience)
            db.session.commit()
            return response_base(message="Success", status=200)
        else:
            return response_base(message="Failed", status=404)
    except Exception as e:
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/experience/view", methods=["POST"])
def view_experience():
    try:
        experience = Experience.query.filter_by(
            id=request.json["experience_id"]
        ).first()
        if experience is not None:
            final_data = {
                "id": experience.id,
                "name": experience.name,
                "icon": experience.icon,
                "is_published": experience.is_published,
                "experience_config": json.loads(experience.experience_config),
                "description": experience.description,
                "devices": [
                    {"id": device.id, "name": device.name}
                    for device in experience.exp_room_device_types
                ],
                "room_types": [
                    {"id": room_type.id, "name": room_type.name}
                    for room_type in experience.exp_room_types
                ],
            }
            return response_base(message="Success", status=200, data=[final_data])
        else:
            return response_base(message="Failed", status=404)
    except Exception as e:
        current_app.logger.error(e)
        return response_base(message="Server error", status=500)


@app.route("/master/devicetype/experience", methods=["POST"])
def device_type_experience():
    rooms = Room.query.filter_by(room_type_id=request.json["room_type_id"]).all()
    print(rooms)
    device_type_data = []
    for room in rooms:
        print(room.room_device_types)
        for device_type in room.room_device_types:
            print(device_type.experience_config)
            device_type_data.append(
                {
                    "id": device_type.id,
                    "name": device_type.name,
                    "technical_name": device_type.technical_name,
                    "experience_config": json.loads(device_type.experience_config),
                }
            )
    # print(device_type_id)
    # final_list = []
    # for device_type in device_types:
    #     data = {
    #         "id": device_type.id,
    #         "name": device_type.name,
    #         "technical_name": device_type.technical_name,
    #     }
    # final_list.append(data)
    return response_base(message="Success", status=200, data=device_type_data)
