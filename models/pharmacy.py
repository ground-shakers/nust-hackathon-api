"""Pharmacy Model
"""

from beanie import Document
from pydantic import Field
from typing import Annotated, Optional

from .helpers import Reviews

class DrugManufacturer(Document):
    """Drug Manufacturer Model"""
    name: Annotated[str, Field(max_length=100)]
    address: Annotated[str, Field(max_length=200)]
    contact_info: Annotated[str, Field(max_length=100, serialization_alias="contactInfo")]
    website: Annotated[Optional[str], Field(max_length=100, serialization_alias="website")]


class Drug(Document):
    """Drugs Model"""
    name: Annotated[str, Field(max_length=100)]
    description: Annotated[str, Field(max_length=500)]
    reviews: Annotated[list[Reviews], Field(default_factory=list)]
    side_effects: Annotated[list[str], Field(default_factory=list, serialization_alias="sideEffects")]
    manufacturer: Annotated[DrugManufacturer, Field()]

class DrugInventory(Document):
    """Drug Inventory Model"""
    drug_id: Annotated[str, Field(serialization_alias="drugId")]
    pharmacy_id: Annotated[str, Field(serialization_alias="pharmacyId")]
    quantity: Annotated[int, Field(ge=0)]
    price: Annotated[float, Field(ge=0.0)]