from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional

class PropertyCreateModel(BaseModel):
    name: str 
    property_master_id: int
    country: str
    state: str
    city: str
    address1: str
    address2: Optional[str] = ""
    banner_base64: str
    logo_base64: str
    zip_code: str
    primary_contact_name: str
    primary_contact_email: EmailStr
    primary_contact_contact_number: str
    primary_contact_job_title: str
    primary_contact_phone_number_code: str

    # @field_validator('name', 'address1', 'address2')
    # def valid_alphanumeric(cls, values):
    #     for field_name, value in values.items():
    #         if not value.isalnum():
    #             raise ValueError(f"{field_name} must be alphanumeric")
    #     return values
    
    # @field_validator('name', 'address1', 'address2')
    # def valid_alphanumeric(cls, v):
    #     if not v.isalnum():
    #         raise ValueError(f"name must be alphanumeric")
    #     return v


    
    @model_validator(mode='before')
    def valid_alphanumerics(cls, values):
        for field_name in ['name', 'address1', 'address2']:
            
            value = values.get(field_name)
            print(value)
            if value and not value.isalnum():
                raise ValueError(f"{field_name} must be alphanumeric")
        return values


    
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