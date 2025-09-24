"""
Appointment response schema.
"""

from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from beanie import PydanticObjectId

class AppointmentInDB(BaseModel):
    """Schema for creating an appointment."""
    id: Annotated[PydanticObjectId, Field()]
    patient: Annotated[str, Field(serialization_alias="patient")]
    doctor: Annotated[str, Field(serialization_alias="doctor")]
    appointment_date: Annotated[
        datetime,
        Field(
            description="Date of the appointment", serialization_alias="appointmentDate"
        ),
    ]
    status: Annotated[
        Literal["scheduled", "completed", "canceled"],
        Field(description="Status of the appointment", serialization_alias="status"),
    ]
    ai_diagnosis: Annotated[
        Optional[str],
        Field(
            description="AI-based diagnosis for the appointment",
            default="",
            serialization_alias="aiDiagnosis",
        ),
    ]
    notes: Annotated[
        Optional[str],
        Field(
            description="Additional notes for the appointment",
            default="",
            serialization_alias="notes",
        ),
    ]

    @field_serializer("id")
    def convert_pydantic_object_id_to_string(self, id: PydanticObjectId) -> str:
        return str(id)
    
        
class AppointmentCreateResponse(BaseModel):
    """Schema for creating an appointment response."""
    message: Annotated[str, Field(default="Appointment created successfully")]
    appointment: Annotated[AppointmentInDB, Field()]