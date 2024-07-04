from pydantic import BaseModel, EmailStr, constr

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

class PropertyUpdateModel(PropertyCreateModel):
    property_id: int

class PropertyFetchModel(BaseModel):
    property_id: int