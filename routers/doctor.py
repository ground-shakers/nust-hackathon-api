"""
This module defines the API routes for patient-related operations.
"""

from utils.api_logger import logger


from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.responses import JSONResponse

from fastapi_limiter.depends import RateLimiter

from beanie import PydanticObjectId
from typing import List, Annotated

from pydantic import ValidationError, Field

from schema.requests.users import DoctorCreateRequest
from schema.responses.users import DoctorResponse, DoctorInDB
from models.users import Admin, Nurse, Doctor

from security.helpers import get_password_hash, get_current_active_user


router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"],
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ],  # Limit to 5 requests per minute per IP
)


@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_new_doctor(request: DoctorCreateRequest):
    """
    Endpoint to create a new doctor.

    Returns the created doctor's details upon success.
    """
    try:
        # Hash the password before storing
        request.password = get_password_hash(request.password)

        new_doctor = Doctor(
            **request.model_dump(exclude=["verify_password", "permissions"]),
            permissions=["me", "get-patient", "get-patients", "get-doctor", "get-appointment"],
        )

        await new_doctor.save()

        doctor_in_db = DoctorInDB(**new_doctor.model_dump())

        logger.info(f"New doctor created with ID: {new_doctor.id}")

        return DoctorResponse(
            message="Account created successfully", doctor=doctor_in_db
        )
    except ValidationError as e:
        logger.error(f"Validation error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Something went wrong"},
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Something went wrong"},
        )


@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: Annotated[
        str, Field(..., max_length=100, description="The ID of the doctor to retrieve")
    ],
    current_user: Annotated[
        Admin | Nurse | Doctor,
        Security(get_current_active_user, scopes=["get-doctor"]),
    ],
):
    """
    Endpoint to retrieve a doctor's details by their ID.
    """
    doctor = await Doctor.get(PydanticObjectId(doctor_id))

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    # Ensure doctors can only access their own data
    if current_user.id != doctor.id and isinstance(current_user, Doctor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this doctor's data",
        )

    doctor_in_db = DoctorInDB(**doctor.model_dump())

    return DoctorResponse(
        message="Doctor retrieved successfully", doctor=doctor_in_db
    )


@router.get("", response_model=List[DoctorInDB])
async def get_doctors(
    current_user: Annotated[Admin, Security(get_current_active_user, scopes=["admin"])],
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Max number of records to return")
):
    """
    Endpoint to retrieve all doctors. 
    
    Returns a list of doctors with pagination support.
    """
    doctors = await Doctor.find(skip=skip, limit=limit).to_list()

    return [DoctorInDB(**doctor.model_dump()) for doctor in doctors]
