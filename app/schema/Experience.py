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
from app.schema.Master import MasterRoomType, MasterDeviceType


# from sqlalchemy import relationship


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    icon = db.Column(db.String(80), nullable=False)
    add_to_home_screen = db.Column(db.Boolean)
    is_published = db.Column(db.Boolean)
    experience_config = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    exp_room_device_types: Mapped[List[MasterDeviceType]] = db.relationship(
        secondary="experience_device"
    )
    exp_room_types: Mapped[List[MasterRoomType]] = db.relationship(
        secondary="experience_room_type"
    )
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Experience {self.name}>"


class ExperienceDevice(db.Model):
    __mapper_args__ = {"confirm_deleted_rows": False}
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(
        db.Integer, db.ForeignKey("experience.id"), nullable=False
    )
    device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_type.id"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<ExperienceDevice {self.id}>"


class ExperienceRoomType(db.Model):
    __mapper_args__ = {"confirm_deleted_rows": False}
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(
        db.Integer, db.ForeignKey("experience.id"), nullable=False
    )
    room_type_id = db.Column(
        db.Integer, db.ForeignKey("master_room_type.id"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<ExperienceDevice {self.id}>"
