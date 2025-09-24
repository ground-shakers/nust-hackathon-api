"""
Appointment request schema.
"""


from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from beanie import PydanticObjectId


class AppointmentCreateRequest(BaseModel):
    """Schema for creating an appointment."""
    patient: Annotated[str, Field(serialization_alias="patient")]
    doctor: Annotated[str, Field(serialization_alias="doctor")]
    appointment_date: Annotated[datetime, Field(description="Date of the appointment", serialization_alias="appointmentDate")]
    ai_diagnosis: Annotated[Optional[str], Field(description="AI-based diagnosis for the appointment", default="", serialization_alias="aiDiagnosis")]
    notes: Annotated[Optional[str], Field(description="Additional notes for the appointment", default="", serialization_alias="notes")]