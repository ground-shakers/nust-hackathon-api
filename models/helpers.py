"""Helper Models for all the other models in the application
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class Address(BaseModel):
    """Address Model"""
    street: Annotated[str, Field(max_length=100)]
    city: Annotated[str, Field(max_length=50)]
    state: Annotated[str, Field(max_length=50)]
    zip: Annotated[str, Field(max_length=10)]

class ContactInfo(BaseModel):
    """Contact Information Model"""
    email: Annotated[EmailStr, Field(max_length=100)]
    phone: Annotated[str, Field(max_length=15)]


class OperationalHours(BaseModel):
    """Operational Hours Model"""

    open_time: Annotated[
        str,
        Field(
            serialization_alias="openTime",
            pattern=r"^(0[1-9]|1[0-2]):([0-5][0-9])(AM|PM)$",
        ),
    ]
    close_time: Annotated[
        str,
        Field(
            serialization_alias="closeTime",
            pattern=r"^(0[1-9]|1[0-2]):([0-5][0-9])(AM|PM)$",
        ),
    ]

class Reviews(BaseModel):
    """
    Reviews Model
    """
    user_id: Annotated[str, Field(max_length=100, serialization_alias="userId")]
    rating: Annotated[float, Field(ge=0, le=5)]
    comment: Annotated[str, Field(max_length=500)]


class BirthDetails(BaseModel):
    """Birth Details Model"""

    day: Annotated[int, Field(ge=1, le=31)]
    month: Annotated[int, Field(ge=1, le=12)]
    year: Annotated[int, Field(ge=1900, le=2100)]
