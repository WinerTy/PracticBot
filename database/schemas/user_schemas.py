import re

from pydantic import BaseModel, validator


class PhoneNumber(BaseModel):
    phone: str

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^\d{11}$", value):
            raise ValueError("Номер телефона должен состоять из 11 цифр.")
        return value


class FullName(BaseModel):
    full_name: str


class UserCreate(BaseModel):
    phone: PhoneNumber
    full_name: FullName
