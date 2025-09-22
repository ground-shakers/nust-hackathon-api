"""User models for the application."""

from pydantic import BaseModel, Field
from typing import Optional, Annotated, Literal

from beanie import Document

from datetime import datetime

from .helpers import ContactInfo, Reviews, BirthDetails
from .treatment import Treatment

from .appointment import Appointment

from .medical_facilities import Pharmacy, Hospital, Clinic

class UserBase(BaseModel):
    """Base Model for all users
    """
    contact_info: Annotated[ContactInfo, Field()]
    password: Annotated[str, Field()]
    first_name: Annotated[str, Field(max_length=50, serialization_alias="firstName")]
    last_name: Annotated[str, Field(max_length=50, serialization_alias="lastName")]
    active: Annotated[bool, Field(default=True)]
    created_at: Annotated[datetime, Field(serialization_alias="createdAt", default_factory=datetime.now)]
    permissions: Annotated[list[str], Field(default_factory=list, serialization_alias="permissions")]
    gender: Annotated[Literal["male", "female", "other"], Field(max_length=10, default=None, serialization_alias="gender")]
    profile_picture: Annotated[Optional[str], Field(default=None, serialization_alias="profilePicture")]
    birth_details: Annotated[BirthDetails, Field(serialization_alias="birthDetails")]

class Patient(UserBase, Document):
    """Patient Model"""
    emergency_contact: Annotated[Optional[str], Field(max_length=15, default=None, serialization_alias="emergencyContact")]
    allergies: Annotated[list[str], Field(default_factory=list, serialization_alias="allergies")]
    medical_history: Annotated[list[str], Field(default_factory=list, serialization_alias="medicalHistory")]
    insurance_provider: Annotated[Optional[str], Field(max_length=100, default=None, serialization_alias="insuranceProvider")]
    insurance_number: Annotated[Optional[str], Field(max_length=50, default=None, serialization_alias="insuranceNumber")]
    diagnoses: Annotated[
        list[str],
        Field(
            default_factory=list,
            serialization_alias="diagnoses",
        ),
    ]
    height: Annotated[Optional[float], Field(ge=0, default=None, serialization_alias="height")]
    weight: Annotated[Optional[float], Field(ge=0, default=None, serialization_alias="weight")]
    treatments: Annotated[list[Optional[Treatment]], Field(default_factory=list, serialization_alias="treatments")]
    appointments: Annotated[list[Appointment], Field(default_factory=list)]

class Doctor(UserBase, Document):
    """Doctor Model"""
    id_number: Annotated[str, Field(max_length=50, serialization_alias="idNumber")]
    specialty: Annotated[list[str], Field(max_length=100, serialization_alias="specialty", default_factory=list)]
    years_of_experience: Annotated[int, Field(ge=0, serialization_alias="yearsOfExperience")]
    patients: Annotated[list[Patient], Field(default_factory=list, serialization_alias="patients")]
    medical_facility: Annotated[Hospital | Clinic, Field(serialization_alias="medicalFacility")]
    reviews: Annotated[list[Reviews], Field(default_factory=list)]
    
    
class Nurse(UserBase, Document):
    """Nurse Model"""
    id_number: Annotated[str, Field(max_length=50, serialization_alias="idNumber")]
    department: Annotated[Optional[str], Field(max_length=100, default=None, serialization_alias="department")]
    years_of_experience: Annotated[int, Field(ge=0, serialization_alias="yearsOfExperience")]
    medical_facility: Annotated[Hospital | Clinic, Field(serialization_alias="medicalFacility")]
    reviews: Annotated[list[Reviews], Field(default_factory=list)]


class Admin(UserBase, Document):
    """Admin Model"""
    pass


class Pharmacist(UserBase, Document):
    """Pharmacist Model"""
    pharmacy: Annotated[Pharmacy, Field(serialization_alias="pharmacy")]