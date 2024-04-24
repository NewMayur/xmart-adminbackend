from app.extensions.db import db
from sqlalchemy.sql import func

# from sqlalchemy import relationship


class KnxDeviceSubTypeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_type.id"), nullable=False
    )
    sub_device_type_id = db.Column(
        db.Integer, db.ForeignKey("master_device_sub_type.id"), nullable=False
    )
    address_name_technical = db.Column(db.String(80), nullable=False)
    address_name = db.Column(db.String(80), nullable=False)
    value_data_type = db.Column(db.String(80), nullable=False)
    vale_data_range = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
