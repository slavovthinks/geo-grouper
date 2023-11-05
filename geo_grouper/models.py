from typing import Optional
from enum import StrEnum, auto

from pydantic import BaseModel


class Location(BaseModel):
    lon: float
    lat: float


class VendorsEnum(StrEnum):
    maps_co = auto()
    geoapify = auto()


class User(BaseModel):
    name: str
    address: str
    location: Optional[Location] = None


class UserGroup(BaseModel):
    center: Location
    users: list[User]


class UploadUserSchema(BaseModel):  # Code repetition is intended in order to separate http logic from core logic
    name: str
    address: str

    def to_app_user(self) -> User:
        return User(name=self.name, address=self.address)


class UserGroupResponseSchema(UserGroup):
    ...


post_json_group_request = list[UploadUserSchema]
post_json_group_response = list[UserGroupResponseSchema]
