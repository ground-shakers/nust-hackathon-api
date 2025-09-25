"""Contains routes related to diagnosis operations.
"""

from utils.api_logger import logger
from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.responses import JSONResponse


from fastapi_limiter.depends import RateLimiter
from beanie import PydanticObjectId
from typing import List, Annotated, Optional


from pydantic import ValidationError, Field
from models.diagnosis import Diagnosis
from schema.requests.diagnosis import DiagnosisCreateRequest


router = APIRouter(
    prefix="/api/v1/diagnoses",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    tags=["Diagnoses"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_diagnosis(request: DiagnosisCreateRequest):
    """Create a new diagnosis.
    
    This endpoint creates a new diagnosis in the system. It does not require authentication.
    """
    try:
        new_diagnosis = Diagnosis(**request.model_dump())
        await new_diagnosis.save()

        logger.info(f"New diagnosis created with ID: {new_diagnosis.id}")

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Diagnosis created successfully",
                "diagnosis": new_diagnosis.model_dump(),
            },
        )
    except ValidationError as e:
        logger.error(f"Validation error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data provided",
        )
    except Exception as e:
        logger.error(f"An error occurred while creating diagnosis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the diagnosis",
        )
        
        
@router.get("/{diagnosis_id}", response_model=Diagnosis)
async def get_diagnosis(
    diagnosis_id: Annotated[
        str, Field(..., max_length=100, description="The ID of the diagnosis to retrieve")
    ],
):
    """
    Endpoint to retrieve a diagnosis's details by their ID.
    """
    try:
        diagnosis = await Diagnosis.get(PydanticObjectId(diagnosis_id))
        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnosis not found",
            )
        return diagnosis
    except ValidationError as e:
        logger.error(f"Validation error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid diagnosis ID format",
        )
    except Exception as e:
        logger.error(f"An error occurred while retrieving diagnosis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the diagnosis",
        )
        
        
@router.get("", response_model=List[Diagnosis])
async def get_diagnoses(
    user_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    """
    Endpoint to retrieve a list of diagnoses.
    """
    try:
        if user_id:
            diagnoses = await Diagnosis.find(Diagnosis.user_id == user_id).limit(limit).skip(skip).to_list()
        else:
            diagnoses = await Diagnosis.find().limit(limit).skip(skip).to_list()
        return diagnoses
    except Exception as e:
        logger.error(f"An error occurred while retrieving diagnoses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving diagnoses",
        )