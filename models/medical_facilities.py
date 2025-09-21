"""Medical Facility Model
"""

from beanie import Document
from pydantic import Field
from typing import Annotated

from .helpers import ContactInfo, Address, OperationalHours, Reviews
from .pharmacy import DrugInventory

class MedicalFacilityBase(Document):
    """Medical Facility Model"""
    name: Annotated[str, Field(max_length=100)]
    address: Annotated[str, Field(max_length=200)]
    contact_info: Annotated[ContactInfo, Field()]
    reviews: Annotated[list[Reviews], Field(default_factory=list)]
    operational_hours: Annotated[
        OperationalHours, Field(serialization_alias="operationalHours")
    ]


class Pharmacy(MedicalFacilityBase):
    """Pharmacy Model"""
    available_drugs: Annotated[
        list[DrugInventory],
        Field(default_factory=list, serialization_alias="availableDrugs"),
    ]

class Clinic(MedicalFacilityBase):
    """Clinic Model"""
    specialties: Annotated[list[str], Field(default_factory=list)]
    doctors: Annotated[list[str], Field(default_factory=list)]


class Hospital(MedicalFacilityBase):
    """Hospital Model"""
    specialties: Annotated[list[str], Field(default_factory=list)]
    doctors: Annotated[list[str], Field(default_factory=list)]