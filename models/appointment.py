"""Appointment Model"""

from beanie import Document
from pydantic import Field
from typing import Annotated

from .users import Patient, Doctor

class Appointment(Document):
    """Appointment Model"""
    patient: Annotated[Patient, Field(serialization_alias="patient")]
    doctor: Annotated[Doctor, Field(serialization_alias="doctor")]
    appointment_date: Annotated[str, Field(description="Date of the appointment", serialization_alias="appointmentDate")]
    status: Annotated[str, Field(description="Status of the appointment", serialization_alias="status")]
    notes: Annotated[str, Field(description="Additional notes for the appointment", default="", serialization_alias="notes")]