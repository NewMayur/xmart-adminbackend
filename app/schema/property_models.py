from pydantic import BaseModel, EmailStr, constr, field_validator

class PropertyCreateModel(BaseModel):
    name: str
    property_master_id: int
    country: str
    state: str
    city: str
    address1: str
    address2: str
    banner_base64: str
    logo_base64: str
    zip_code: str
    primary_contact_name: str
    primary_contact_email: EmailStr
    primary_contact_contact_number: str
    primary_contact_job_title: str
    primary_contact_phone_number_code: str

    @field_validator('primary_contact_contact_number')
    def validate_contact_number(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError('Contact number must be a 10-digit')
        return v


class PropertyUpdateModel(BaseModel):
    property_id: int
    name: str
    property_master_id: int
    country: str
    state: str
    city: str
    address1: str
    address2: str
    banner_base64: str
    logo_base64: str
    zip_code: str
    primary_contact_name: str
    primary_contact_email: EmailStr
    primary_contact_contact_number: str
    primary_contact_job_title: str
    primary_contact_contact_number_code: str

    @field_validator('primary_contact_contact_number')
    def validate_contact_number(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError('Contact number must be a 10-digit')
        return v