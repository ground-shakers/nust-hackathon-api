"""
User-related request schemas
"""
import re

from fastapi import HTTPException, status

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, Annotated, Literal, Self

from datetime import datetime

from models.helpers import ContactInfo, BirthDetails

class UserCreateRequestBase(BaseModel):
    contact_info: Annotated[ContactInfo, Field()]
    password: Annotated[str, Field()]
    verify_password: Annotated[str, Field()]
    first_name: Annotated[str, Field(max_length=50, serialization_alias="firstName")]
    last_name: Annotated[str, Field(max_length=50, serialization_alias="lastName")]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(max_length=10, default=None, serialization_alias="gender"),
    ]
    birth_details: Annotated[BirthDetails, Field(serialization_alias="birthDetails")]

    # * Validate the password to ensure it has at least one uppercase letter,
    # * one special character, one lowercase letter, and one number
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contain at least one uppercase letter",
            )
        if not re.search(r"[a-z]", v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contain at least one lowercase letter",
            )
        if not re.search(r"\d", v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contain at least one number",
            )
        if not re.search(r"[@$!%*?&#]", v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must contain at least one special character",
            )
        return v

    # * Check if password and verify password fields match
    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        password = self.password
        verify_password = self.verify_password

        if (
            password is not None
            and verify_password is not None
            and password != verify_password
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Passwords do not match",
            )
        return self

    # * Check if first name and last name in password
    @model_validator(mode="after")
    def check_first_name_last_name_in_password(self) -> Self:
        first_name = self.first_name
        last_name = self.last_name
        password = self.password

        if first_name in password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password contains first name",
            )
        if last_name in password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password contains last name",
            )
        return self


class PatientCreateRequest(UserCreateRequestBase):
    """Patient Creation Request Schema"""