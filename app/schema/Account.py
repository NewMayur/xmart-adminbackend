from app.extensions.db import db
from sqlalchemy.sql import func

# from sqlalchemy import relationship


class AccountProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(80), nullable=False)
    company_name = db.Column(db.String(80), nullable=False)
    company_domain = db.Column(db.String(80), nullable=False)
    company_address = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    pin = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # deleted_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Building {self.name}>"
