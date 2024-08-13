from app.extensions.db import db
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class MasterRoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    technical_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Room {self.name}>"


class MasterSubRoomType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    technical_name = db.Column(db.String(80), nullable=False)
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<SubRoomType {self.name}>"


class MasterDeviceType(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    technical_name = db.Column(db.String(80), nullable=False)
    experience_config = db.Column(db.String(255), nullable=False, default='{}')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))
    device_sub_type_1 = db.relationship(
        "MasterDeviceSubType", backref="master_device_sub_type_1"
    )

    def __repr__(self):
        return f"<MasterDeviceType {self.name}>"


class MasterProtocol(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<MasterDeviceType {self.name}>"


class MasterDeviceSubType(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    technical_name = db.Column(db.String(80), nullable=False)
    master_device_type_id = db.Column(db.Integer, db.ForeignKey('master_device_type.id'), nullable=False)
    master_device_type_new = db.relationship(
        "MasterDeviceType", backref="master_device_type_new"
    )
    icon_id = db.Column(db.Integer, db.ForeignKey('icon.id'), nullable=False)
    icon = db.relationship('Icon', foreign_keys="Icon.device_sub_type_id", back_populates="device_sub_type")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<MasterDeviceSubType {self.name}>"

class Icon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    file_path = db.Column(db.String(255), nullable=False)
    device_sub_type_id = db.Column(db.Integer, db.ForeignKey('master_device_sub_type.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    device_sub_type = db.relationship('MasterDeviceSubType', foreign_keys=[device_sub_type_id], backref='icons')

    def __repr__(self):
        return f"<Icon {self.filename}>"