from flask import current_app
from flask import request, jsonify, url_for
from server import app, bcrypt
from app.schema.User import User
from app.schema.Property import Property, PropertyContact
from app.extensions.db import db
from app.extensions.responses import response_base
import base64
import uuid
from app.extensions.utils import save_base64_file


@app.route("/property/create", methods=["POST"])
def property():
    # Save image to file system
    if request.json["banner_base64"] != "":
        banner_path = save_base64_file(request.json["banner_base64"])
    else:
        pass
    if request.json["logo_base64"] != "":
        logo_path = save_base64_file(request.json["logo_base64"])
    else:
        pass
    property = Property(
        name=request.json["name"],
        property_type_master_id=request.json["property_master_id"],
        country_master_id=request.json["country_id"],
        state_master_id=request.json["state_id"],
        city_master_id=request.json["city_id"],
        address1=request.json["address1"],
        address2=request.json["address2"],
        banner_image_path=banner_path,
        logo_image_path=logo_path,
    )
    db.session.add(property)
    db.session.commit()
    contact = PropertyContact(
        name=request.json["primary_contact_name"],
        email=request.json["primary_contact_email"],
        phone_number=request.json["primary_contact_contact_number"],
        job_title=request.json["primary_contact_job_title"],
        property_id=property.id,
    )
    db.session.add(contact)
    db.session.commit()

    return response_base(message="Success", status=200)


@app.route("/property/view", methods=["POST"])
def property_fetch():
    import os

    # print(os.path.abspath(os.path.dirname(__file__)))
    property = Property.query.get_or_404(request.json["property_id"])
    data = {
        "name": property.name,
        "property_type": property.property_type.name,
        "property_type_id": property.property_type_master_id,
        # "country": property.country.name,
        # "country_id": property.country_master_id,
        # "state": property.state.name,
        # "state_id": property.state_master_id,
        # "city": property.city.name,
        # "city_id": property.city_master_id,
        "address1": property.address1,
        "address2": property.address2,
        "primary_contact_name": property.property_contact[0].name,
        "primary_contact_job_title": property.property_contact[0].job_title,
        "primary_contact_email": property.property_contact[0].email,
        "primary_contact_contact_number": property.property_contact[0].phone_number,
        "banner_url": app.config["IMAGE_URL"] + property.banner_image_path,
    }
    return response_base(message="Success", status=200, data=[data])


@app.route("/images")
def flask_logo():
    return current_app.send_static_file(request.args.get("image_name"))
