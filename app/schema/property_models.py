from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class PropertyCreateModel(BaseModel):
    name: str 
    property_master_id: int
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
    address1: str
    address2: Optional[str] = ""
    banner_base64: str
    logo_base64: str
    zip_code: Optional[str] = Field("", max_length=5)
    primary_contact_name: Optional[str] = Field("", max_length=50)
    primary_contact_email: EmailStr
    primary_contact_contact_number: str
    primary_contact_job_title: Optional[str] = Field("", max_length=50)
    primary_contact_phone_number_code: Optional[str] = Field("", max_length=3)
    
    # @field_validator("name","address1")
    # @classmethod
    # def valid_alphanumeric(cls, v: str, info: ValidationInfo):
    #     # if info.field_name == 'name':
    #     #     if not name_pattern.match(v): raise ValueError(f'{v} is not a valid name.')
    #     print(v)
    #     if (info.field_name == 'name') and (not v.isalnum()):
    #         raise ValueError(f"{v} must be alphanumeric")
    #     if (info.field_name == 'address1') and (not v.isalnum()):
    #         raise ValueError(f"{v} must be alphanumeric")
    #     return v

    @field_validator('name', 'address1', 'address2')
    def valid_alphanum(cls, v, info):
        if not v.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return v
    
    @field_validator('primary_contact_contact_number')
    def validate_contact_number(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError("Please enter a valid 10-digit phone number.")
        return v


class PropertyUpdateModel(BaseModel):
    property_id: int
    name: str 
    property_master_id: int
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
    address1: str
    address2: Optional[str] = ""
    banner_base64: str
    logo_base64: str
    zip_code: Optional[str] = Field("", max_length=5)
    primary_contact_name: Optional[str] = Field("", max_length=50)
    primary_contact_email: EmailStr
    primary_contact_contact_number: str
    primary_contact_job_title: Optional[str] = Field("", max_length=50)
    primary_contact_contact_number_code: Optional[str] = Field("", max_length=3)

    @field_validator('name', 'address1', 'address2')
    def valid_alphanum(cls, v, info):
        if not v.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return v
    
    @field_validator('primary_contact_contact_number')
    def validate_contact_number(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError("Please enter a valid 10-digit phone number.")
        return v