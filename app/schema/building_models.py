from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class FloorModel(BaseModel):
    name: str = Field(..., max_length=50)
    floor_number: str = Field(..., max_length=50)
    id: Optional[int] = 0

    @field_validator('name', 'floor_number')
    def valid_alphanumerics(cls, v, info):
        if not v.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return v

class BuildingCreateModel(BaseModel):
    name: str = Field(..., max_length=50)
    building_number: str = Field(..., max_length=50)
    number_of_floors: int = Field(0, gt=0)
    property_id: int = Field(..., gt=0)
    floors: List[FloorModel]

    @field_validator('name', 'building_number')
    def valid_alphanumerics(cls, v, info):
        if not v.isalnum():
            raise ValueError(f"{info.field_name} must be alphanumeric")
        return v

class BuildingEditModel(BuildingCreateModel):
    building_id: int = Field(..., gt=0)


class BuildingViewModel(BaseModel):
    building_id: int = Field(..., gt=0)

class BuildingListModel(BaseModel):
    property_id: int = Field(..., gt=0)

class BuildingDeleteModel(BaseModel):
    building_id: int = Field(..., gt=0)

class FloorListModel(BaseModel):
    property_id: int = Field(..., gt=0)
    building_id: int = Field(..., gt=0)