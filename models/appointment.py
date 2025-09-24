"""Appointment Model"""

from beanie import PydanticObjectId

from beanie import Document
from pydantic import Field, field_serializer
from typing import Annotated, Optional, Literal
from datetime import datetime

class Appointment(Document):
    """Appointment Model"""
    patient: Annotated[str, Field(serialization_alias="patient")]
    doctor: Annotated[str, Field(serialization_alias="doctor")]
    appointment_date: Annotated[datetime, Field(description="Date of the appointment", serialization_alias="appointmentDate")]
    status: Annotated[Literal["scheduled", "completed", "canceled"], Field(description="Status of the appointment", default="scheduled")]
    ai_diagnosis: Annotated[Optional[str], Field(description="AI-based diagnosis for the appointment", default="", serialization_alias="aiDiagnosis")]
    notes: Annotated[Optional[str], Field(description="Additional notes for the appointment", default="", serialization_alias="notes")]

    @field_serializer("id")
    def convert_pydantic_object_id_to_string(self, id: PydanticObjectId) -> str:
        return str(id)