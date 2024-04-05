from app.extensions.db import db
from sqlalchemy.sql import func

# from sqlalchemy import relationship


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))
    banner_image_path = db.Column(db.String(100))
    logo_image_path = db.Column(db.String(100))
    property_type_master_id = db.Column(
        db.Integer, db.ForeignKey("master_property_type.id"), nullable=False
    )
    country_master_id = db.Column(
        db.Integer, db.ForeignKey("master_country.id"), nullable=False
    )
    state_master_id = db.Column(
        db.Integer, db.ForeignKey("master_state.id"), nullable=False
    )
    city_master_id = db.Column(
        db.Integer, db.ForeignKey("master_city.id"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # country = db.relationship(
    #     "CountryMaster", backref=backref("country_master", uselist=False))
    property_type = db.relationship(
        "MasterPropertyType", backref="master_property_type"
    )
    country = db.relationship("MasterCountry", backref="country_master")
    state = db.relationship("MasterState", backref="state_master")
    city = db.relationship("MasterCity", backref="city_master")
    property_contact = db.relationship("PropertyContact", backref="property_contact")

    def __repr__(self):
        return f"<Property {self.name}>"


class PropertyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    job_title = db.Column(db.String(80), unique=False, nullable=False)
    phone_number = db.Column(db.String(80), unique=False, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PropertyContact {self.name}>"


class MasterPropertyType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PropertyMater {self.name}>"


class MasterCountry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Country {self.name}>"


class MasterState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<State {self.name}>"


class MasterCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<City {self.name}>"
