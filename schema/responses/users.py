"""User-related response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Annotated, Literal

from datetime import datetime

from models.helpers import ContactInfo, BirthDetails
from models.treatment import Treatment

from models.appointment import Appointment

class PatientInDB(BaseModel):
    id: Annotated[str, Field()]
    first_name: Annotated[str, Field(max_length=50, serialization_alias="firstName")]
    last_name: Annotated[str, Field(max_length=50, serialization_alias="lastName")]
    contact_info: Annotated[ContactInfo, Field(serialization_alias="contactInfo")]
    created_at: Annotated[
        datetime,
        Field(serialization_alias="createdAt", default_factory=datetime.now),
    ]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(max_length=10, default=None, serialization_alias="gender"),
    ]
    profile_picture: Annotated[
        Optional[str], Field(default=None, serialization_alias="profilePicture")
    ]
    birth_details: Annotated[BirthDetails, Field(serialization_alias="birthDetails")]
    emergency_contact: Annotated[
        Optional[str],
        Field(max_length=15, default=None, serialization_alias="emergencyContact"),
    ]
    allergies: Annotated[
        list[str], Field(default_factory=list, serialization_alias="allergies")
    ]
    medical_history: Annotated[
        list[str], Field(default_factory=list, serialization_alias="medicalHistory")
    ]
    insurance_provider: Annotated[
        Optional[str],
        Field(max_length=100, default=None, serialization_alias="insuranceProvider"),
    ]
    insurance_number: Annotated[
        Optional[str],
        Field(max_length=50, default=None, serialization_alias="insuranceNumber"),
    ]
    diagnoses: Annotated[
        list[str],
        Field(
            default_factory=list,
            serialization_alias="diagnoses",
        ),
    ]
    height: Annotated[
        Optional[float], Field(ge=0, default=None, serialization_alias="height")
    ]
    weight: Annotated[
        Optional[float], Field(ge=0, default=None, serialization_alias="weight")
    ]
    treatments: Annotated[
        list[Optional[Treatment]],
        Field(default_factory=list, serialization_alias="treatments"),
    ]
    appointments: Annotated[list[Appointment], Field(default_factory=list)]


class DoctorInDB(BaseModel):
    id: Annotated[str, Field()]
    first_name: Annotated[str, Field(max_length=50, serialization_alias="firstName")]
    last_name: Annotated[str, Field(max_length=50, serialization_alias="lastName")]
    contact_info: Annotated[ContactInfo, Field(serialization_alias="contactInfo")]
    created_at: Annotated[
        datetime,
        Field(serialization_alias="createdAt", default_factory=datetime.now),
    ]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(max_length=10, default=None, serialization_alias="gender"),
    ]
    profile_picture: Annotated[
        Optional[str], Field(default=None, serialization_alias="profilePicture")
    ]
    birth_details: Annotated[BirthDetails, Field(serialization_alias="birthDetails")]
    id_number: Annotated[str, Field(max_length=50, serialization_alias="idNumber")]
    specialty: Annotated[
        list[str],
        Field(max_length=100, serialization_alias="specialty", default_factory=list),
    ]
    years_of_experience: Annotated[int, Field(ge=0, serialization_alias="yearsOfExperience")]
    patients: Annotated[list, Field(default_factory=list, serialization_alias="patients")]
    medical_facility: Annotated[str, Field(serialization_alias="medicalFacility")]
    reviews: Annotated[list, Field(default_factory=list)]
    appointments: Annotated[list[str], Field(default_factory=list)]

class PatientResponse(BaseModel):
    """Response Model for Patient"""
    message: Annotated[str, Field(default="Account created successfully")]
    patient: Annotated[PatientInDB, Field()]
    
    
class DoctorResponse(BaseModel):
    """Response Model for Doctor"""
    message: Annotated[str, Field(default="Account created successfully")]
    doctor: Annotated[DoctorInDB, Field()]