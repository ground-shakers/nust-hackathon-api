"""
This module defines the API routes for patient-related operations.
"""

from utils.api_logger import logger


from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.responses import JSONResponse

from beanie import PydanticObjectId
from typing import List, Annotated

from fastapi_limiter.depends import RateLimiter

from pydantic import ValidationError, Field

from schema.requests.users import PatientCreateRequest
from schema.responses.users import PatientInDB, PatientResponse
from models.users import Patient, Pharmacist, Admin, Nurse, Doctor

from security.helpers import get_password_hash, get_current_active_user


router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"],
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ],  # Limit to 5 requests per minute per IP
)


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_new_patient(request: PatientCreateRequest):
    """
    Endpoint to create a new patient.

    Returns the created patient's details upon success.
    """
    try:
        # Hash the password before storing
        request.password = get_password_hash(request.password)

        new_patient = Patient(
            **request.model_dump(exclude=["verify_password", "permissions"]),
            permissions=["me", "get-patient"],
        )

        await new_patient.save()

        patient_in_db = PatientInDB(**new_patient.model_dump())

        logger.info(f"New patient created with ID: {new_patient.id}")

        return PatientResponse(
            message="Account created successfully",
            patient=patient_in_db
        )
    except ValidationError as e:
        logger.error(f"Validation error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Something went wrong {e}"},
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Something went wrong {e}"},
        )


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: Annotated[str, Field(..., max_length=100, description="The ID of the patient to retrieve")], current_user: Annotated[Patient | Pharmacist | Admin | Nurse | Doctor, Security(get_current_active_user, scopes=["get-patient"])]):
    """
    Endpoint to retrieve a patient's details by their ID.
    """
    patient = await Patient.get(patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Ensure patients can only access their own data
    if current_user.id != patient_id and isinstance(current_user, Patient):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this patient's data"
        )

    patient_in_db = PatientInDB(**patient.model_dump())

    return PatientResponse(
        message="Patient retrieved successfully",
        patient=patient_in_db
    )


@router.get("", response_model=List[PatientInDB])
async def get_patients(current_user: Annotated[Admin | Nurse | Doctor, Security(get_current_active_user, scopes=["get-patients"])], skip: int = Query(0, ge=0, description="Number of records to skip"), limit: int = Query(10, le=100, description="Max number of records to return")):
    """
    Endpoint to retrieve all patients.
    """
    patients = await Patient.find(skip=skip, limit=limit).to_list()

    return [PatientInDB(**patient.model_dump()) for patient in patients]
