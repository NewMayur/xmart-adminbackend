from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from app.extensions.db import db
from sqlalchemy.sql import func
from app.schema.Master import MasterSubRoomType, MasterDeviceType


# from sqlalchemy import relationship


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey("building.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey("floor.id"), nullable=False)
    room_type_id = db.Column(
        db.Integer, db.ForeignKey("master_room_type.id"), nullable=False
    )
    room_type = db.relationship("MasterRoomType", backref="room_type")
    floors = db.relationship("Floor", backref="room")
    # building = db.relationship("Building", backref="room")
    buildings = db.relationship("Building", backref="building")
    room_sub_types: Mapped[List[MasterSubRoomType]] = db.relationship(
        secondary="room_room_sub_type"
    )
    room_device_types: Mapped[List[MasterDeviceType]] = db.relationship(
        secondary="room_device_type"
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Room {self.name}>"


class RoomRoomSubType(db.Model):
    __mapper_args__ = {"confirm_deleted_rows": False}
    id: Mapped[int] = mapped_column(primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    room_sub_type_id = db.Column(
        db.Integer, db.ForeignKey("master_sub_room_type.id"), nullable=False
    )
    # room = db.relationship("Room", backref="rooms")
    # room_sub_type = db.relationship("MasterSubRoomType", backref="master_sub_room_type")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class RoomDevice(db.Model):
    __mapper_args__ = {"confirm_deleted_rows": False}
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_type.id"), nullable=False
    )
    device_sub_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_sub_type.id"), nullable=True
    )
    room_sub_type_id = db.Column(
        db.Integer, db.ForeignKey("master_sub_room_type.id"), nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    group_name = db.Column(db.String(80), nullable=False)
    # device_make = db.Column(db.String(80), nullable=False)
    # device_model = db.Column(db.String(80), nullable=False)
    # device_ip = db.Column(db.String(80), nullable=False)
    device_meta = db.Column(db.Text, nullable=False)
    device_config = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean)
    is_group = db.Column(db.Boolean)
    add_to_home_screen = db.Column(db.Boolean)
    remark = db.Column(db.String(255))
    icon = db.Column(db.String(80))
    room_number = db.Column(db.String(80), nullable=False)
    is_service = db.Column(db.Boolean)
    floor_id = db.Column(db.Integer, db.ForeignKey("floor.id"), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey("building.id"), nullable=False)
    protocol_id = db.Column(db.Integer, db.ForeignKey("master_protocol.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    room_sub_type = db.relationship("MasterSubRoomType", backref="master_sub_room_type")
    device_sub_type = db.relationship(
        "MasterDeviceSubType", backref="master_device_sub_type"
    )
    device_type = db.relationship("MasterDeviceType", backref="master_device_type")
    protocol = db.relationship("MasterProtocol", backref="master_protocol")


class RoomDeviceType(db.Model):
    __mapper_args__ = {"confirm_deleted_rows": False}
    # id = db.Column(db.Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_type.id"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
