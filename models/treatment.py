"""Treatment Model
"""

from beanie import Document, PydanticObjectId
from pydantic import Field, field_serializer
from typing import Annotated

from datetime import datetime
from .pharmacy import Drug


class Treatment(Document):
    """Treatment Model"""
    patient_id: Annotated[str, Field(serialization_alias="patientId")]
    doctor_id: Annotated[str, Field(serialization_alias="doctorId")]
    medication: Annotated[Drug, Field()]
    dosage: Annotated[str, Field(max_length=100)]
    frequency: Annotated[str, Field(max_length=100)]
    start_date: Annotated[datetime, Field(default_factory=datetime.now, serialization_alias="startDate")]
    end_date: Annotated[datetime, Field(default_factory=datetime.now, serialization_alias="endDate")]
    notes: Annotated[str | None, Field(max_length=500, default=None)]