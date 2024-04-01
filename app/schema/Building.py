from app.extensions.db import db
from sqlalchemy.sql import func

# from sqlalchemy import relationship


class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    number_of_floors = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    floors = db.relationship("Floor", backref="floor")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Building {self.name}>"


class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey("building.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    rooms = db.relationship("Room", backref="room")
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Floor {self.name}>"
