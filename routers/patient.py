"""
This module defines the API routes for patient-related operations.
"""


from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from typing import List

from schema.requests.users import PatientCreateRequest
from models.users import Patient
from security.helpers import get_password_hash


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post("")
async def create_new_patient(request: PatientCreateRequest):
    """
    Endpoint to create a new patient.
    """
    
    # Hash the password before storing
    request.password = get_password_hash(request.password)
    
    new_patient = Patient(
        **request.model_dump(exclude=["verify_password"]),
        permissions=["me"]
    )

    await new_patient.save()
    
    return {"message": "Patient created successfully", "patient_id": str(new_patient.id)}