from pathlib import Path

from flask import current_app
from flask import request, jsonify, url_for
from pydantic_flask import validate
from pydantic import ValidationError



from app.schema.Room import Room
from server import app, bcrypt
from app.schema.User import User
from app.schema.Property import Property, PropertyContact
from app.schema.Building import Building, Floor
from app.schema.Room import RoomRoomSubType, RoomDevice,RoomDeviceType
from app.extensions.db import db
from app.extensions.responses import response_base
import base64
import uuid
from app.extensions.utils import save_base64_file

from app.schema.property_models import *

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(ENV_FILE_PATH)

@app.route("/property/create", methods=["POST"])
def create_property():
    try:
        data = PropertyCreateModel(**request.json)
    except ValidationError as e:
        error_messages = [error['msg'] for error in e.errors()]
        return response_base(message="Bad Request", status=400, data={"Errors" :error_messages})

    property_exist = Property.query.all()
    if len(property_exist) > 0:
        return response_base(message="Property already exists", status=409, data=[])

    banner_path = save_base64_file(data.banner_base64) if data.banner_base64 else ""
    logo_path = save_base64_file(data.logo_base64) if data.logo_base64 else ""

    property = Property(
        name=data.name,
        property_type_master_id=data.property_master_id,
        country=data.country,
        state=data.state,
        city=data.city,
        address1=data.address1,
        address2=data.address2,
        banner_image_path=banner_path,
        logo_image_path=logo_path,
        zip_code=data.zip_code,
    )
    db.session.add(property)
    db.session.flush()

    contact = PropertyContact(
        name=data.primary_contact_name,
        email=data.primary_contact_email,
        phone_number=data.primary_contact_contact_number,
        job_title=data.primary_contact_job_title,
        phone_number_code=data.primary_contact_phone_number_code,
        property_id=property.id,
    )
    db.session.add(contact)
    db.session.commit()

    return response_base(message="Success", status=200, data=[property.id])


@app.route("/property/view", methods=["POST"])
def property_fetch():
    property = Property.query.filter_by(id=request.json["property_id"]).first()
    print(request.json["property_id"])
    if not property:
        return response_base(message="Failed", status=404, data=[])
    data = {
        "name": property.name,
        "property_type": property.property_type.name,
        "property_master_id": property.property_type_master_id,
        "country": property.country,
        # "country_id": property.country_master_id,
        "state": property.state,
        # "state_id": property.state_master_id,
        "city": property.city,
        "zip_code": property.zip_code,
        # "city_id": property.city_master_id,
        "address1": property.address1,
        "address2": property.address2,
        "primary_contact_name": property.property_contact[0].name,
        "primary_contact_job_title": property.property_contact[0].job_title,
        "primary_contact_email": property.property_contact[0].email,
        "primary_contact_contact_number": property.property_contact[0].phone_number,
        "primary_contact_contact_number_code": property.property_contact[
            0
        ].phone_number_code,
        "banner_base64": app.config["IMAGE_URL"] + property.banner_image_path,
        "logo_base64": app.config["IMAGE_URL"] + property.logo_image_path,
        # "banner_url": property.banner_image_path,
    }
    return response_base(message="Success", status=200, data=[data])


@app.route("/property/list", methods=["GET"])
def property_list():
    # print("property_id",request.json["property_id"])
    properties = Property.query.all()
    if len(properties) == 0:
        return response_base(message="Success", status=200, data=[])
    else:
        pass
    property_list = []
    for property in properties:
        buildings = Building.query.filter_by(property_id=property.id).all()
        # print(buildings.floors)
        no_of_buildings = len(buildings)
        no_of_floors = 0
        no_of_rooms = 0
        for building in buildings:
            for floor in building.floors:
                no_of_floors = no_of_floors + 1
                no_of_rooms = no_of_rooms + len(floor.rooms)
        print(no_of_floors)
        print(no_of_rooms)
        print(no_of_buildings)
        data = {
            "property_id": property.id,
            "name": property.name,
            "property_type": property.property_type.name,
            "property_master_id": property.property_type_master_id,
            "country": property.country,
            # "country_id": property.country_master_id,
            "state": property.state,
            # "state_id": property.state_master_id,
            "city": property.city,
            "zip_code": property.zip_code,
            # "city_id": property.city_master_id,
            "address1": property.address1,
            "address2": property.address2,
            "primary_contact_name": property.property_contact[0].name,
            "primary_contact_job_title": property.property_contact[0].job_title,
            "primary_contact_email": property.property_contact[0].email,
            "primary_contact_contact_number": property.property_contact[0].phone_number,
            "primary_contact_contact_number_code": property.property_contact[
                0
            ].phone_number_code,
            "banner_base64": app.config["IMAGE_URL"] + property.banner_image_path,
            "logo_base64": app.config["IMAGE_URL"] + property.logo_image_path,
            "buildings": no_of_buildings,
            "floors": no_of_floors,
            "rooms": no_of_rooms,
            # "banner_url": property.banner_image_path,
        }
        property_list.append(data)
    return response_base(message="Success", status=200, data=property_list)


@app.route("/property/edit", methods=["POST"])
def edit_property():
    try:
        data = PropertyUpdateModel(**request.json)
    except ValidationError as e:
        error_messages = [error['msg'] for error in e.errors()]
        return response_base(message="Bad Request", status=400, data={"Errors" : error_messages})

    property = Property.query.filter_by(id=data.property_id).first()
    if not property:
        return response_base(message="Failed", status=404, data=[])

    # Save image to file system
    banner_path = save_base64_file(data.banner_base64) if data.banner_base64 else ""
    logo_path = save_base64_file(data.logo_base64) if data.logo_base64 else ""

    property.name = data.name
    property.property_type_master_id = data.property_master_id
    property.country = data.country
    property.state = data.state
    property.city = data.city
    property.zip_code = data.zip_code
    property.address1 = data.address1
    property.address2 = data.address2
    property.banner_image_path = banner_path
    property.logo_image_path = logo_path

    contact = property.property_contact[0]
    contact.name = data.primary_contact_name
    contact.job_title = data.primary_contact_job_title
    contact.email = data.primary_contact_email
    contact.phone_number = data.primary_contact_contact_number
    contact.phone_number_code = data.primary_contact_contact_number_code

    db.session.add(property)
    db.session.add(contact)
    db.session.commit()

    return response_base(message="Success", status=200, data=[property.id])
@app.route("/property/delete", methods=["DELETE"])
def property_delete():
    property = Property.query.filter_by(id=request.json["property_id"]).first()
    if not property:
        return response_base(message="Failed", status=404, data=[])
    else:
        pass
    buildings = Building.query.filter_by(property_id=property.id).all()
    for building in buildings:
        for floor in building.floors:
            print(floor.id,"floors")
            for room in floor.rooms:
                print(room.id)
                sub_rooms = RoomRoomSubType.query.filter_by(room_id=room.id).all()
                for sub_room in sub_rooms:
                    db.session.delete(sub_room)
                room_devices = RoomDevice.query.filter_by(room_id=room.id).all()
                for dev in room_devices:
                    # print(dev)
                    db.session.delete(dev)
                room_device_types = RoomDeviceType.query.filter_by(room_id=room.id).all()
                print(len(room_device_types),"types", room.id)
                for room_device_type in room_device_types:
                    db.session.delete(room_device_type)
                db.session.delete(room)
            # print("floors", floor.id)
            db.session.delete(floor)
        db.session.delete(building)
    db.session.delete(property.property_contact[0])
    db.session.delete(property)
    db.session.commit()
    return response_base(message="Success", status=200, data=[])


@app.route("/images")
def flask_logo():
    return current_app.send_static_file(request.args.get("image_name"))
