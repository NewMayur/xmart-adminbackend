from app.extensions.db import db
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class MasterRoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Room {self.name}>"


class MasterSubRoomType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

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
    master_device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_type.id"), nullable=False
    )
    protocol_id = db.Column(
        db.Integer, db.ForeignKey("master_protocol.id"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<MasterDeviceSubType {self.name}>"


# class MasterKnxAddressName(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
#     updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

#     def __repr__(self):
#         return f"<MasterKNXAddressName {self.name}>"


# class MasterValueDataType(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
#     updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

#     def __repr__(self):
#         return f"<MasterKnxValueDataType {self.name}>"


# class MasterDataTypeRange(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
#     updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

#     def __repr__(self):
#         return f"<MasterKnxRange {self.name}>"
