"""Appointment Model"""

from beanie import PydanticObjectId

from beanie import Document
from pydantic import Field, field_serializer
from typing import Annotated

class Appointment(Document):
    """Appointment Model"""
    patient: Annotated[str, Field(serialization_alias="patient")]
    doctor: Annotated[str, Field(serialization_alias="doctor")]
    appointment_date: Annotated[str, Field(description="Date of the appointment", serialization_alias="appointmentDate")]
    status: Annotated[str, Field(description="Status of the appointment", serialization_alias="status")]
    notes: Annotated[str, Field(description="Additional notes for the appointment", default="", serialization_alias="notes")]

    @field_serializer("id")
    def convert_pydantic_object_id_to_string(self, id: PydanticObjectId) -> str:
        return str(id)