"""
Appointment Router with all the routes for managing appointments.
"""


from utils.api_logger import logger

from fastapi import APIRouter, Depends, HTTPException, status, Security, Query, BackgroundTasks
from fastapi.responses import JSONResponse

from fastapi_limiter.depends import RateLimiter
from beanie import PydanticObjectId
from typing import List, Annotated, Optional

from pydantic import ValidationError, Field

from models.appointment import Appointment
from schema.responses.appointment import AppointmentInDB, AppointmentCreateResponse
from schema.requests.appointment import AppointmentCreateRequest

from utils.background_tasks import notify_appointment_creation

from models.users import Patient, Doctor

from beanie.operators import And
from beanie.exceptions import DocumentNotFound


router = APIRouter(
    prefix="/api/v1/appointments",
   tags=["Appointments"],
   dependencies=[Depends(RateLimiter(times=5, seconds=60))],  # Limit to 5 requests per minute per IP
)


@router.post("", response_model=AppointmentCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(request: AppointmentCreateRequest, background_tasks: BackgroundTasks):
    """Create a new appointment.

    This endpoint creates a new appointment in the system. It does not require authentication.
    Due to the time constraints of the hackathon, error handling is minimal.
    """
    
    try:
        new_appointment = Appointment(**request.model_dump())
        patient_in_db = await Patient.get(PydanticObjectId(new_appointment.patient))
        doctor_in_db = await Doctor.get(PydanticObjectId(new_appointment.doctor))

        if not patient_in_db:
            logger.error(f"Patient with ID {new_appointment.patient} not found.")
            return
        
        if not doctor_in_db:
            logger.error(f"Doctor with ID {new_appointment.doctor} not found.")
            return

        await new_appointment.save()

        patient_in_db.appointments.append(str(new_appointment.id))
        doctor_in_db.appointments.append(str(new_appointment.id))

        await patient_in_db.save()
        await doctor_in_db.save()

        appointment_in_db = AppointmentInDB(**new_appointment.model_dump())

        background_tasks.add_task(notify_appointment_creation, appointment=appointment_in_db)
        
        return AppointmentCreateResponse(message="Appointment created successfully", appointment=appointment_in_db)
    except ValidationError as e:
        logger.error(f"Validation error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong: {e}")
    
    
@router.get("/{appointment_id}", response_model=AppointmentInDB, status_code=status.HTTP_200_OK)
async def get_appointment(appointment_id: str):
    """Get an appointment by ID.
    
    This endpoint retrieves an appointment by its ID. It does not require authentication.
    Due to the time constraints of the hackathon, error handling is minimal.
    
    **appointment_id**: The ID of the appointment to retrieve.
    """ 
    try:
        appointment = await Appointment.get(PydanticObjectId(appointment_id))
        
        if not appointment:
            raise DocumentNotFound
        
        return AppointmentInDB(**appointment.model_dump())
    except DocumentNotFound:
        
        logger.error("Appointment not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment not found: {e}")
    except Exception as e:
        
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong: {e}")


@router.get("", response_model=List[AppointmentInDB], status_code=status.HTTP_200_OK)
async def get_appointments(
    doctor_id: Annotated[Optional[str], Query(description="Filter by doctor ID")] = None,
    patient_id: Annotated[Optional[str], Query(description="Filter by patient ID")] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    """Get appointments from the system.

    This endpoint has pagination support. It does not require authentication.
    Due to the time constraints of the hackathon, error handling is minimal.
    
    Returns a list of appointments.
    
    **skip**: Number of records to skip (default is 0).
    **limit**: Maximum number of records to return (default is 10, max is 100).
    **doctor_id**: Filter appointments by doctor ID (optional).
    **patient_id**: Filter appointments by patient ID (optional).
    """
    try:
        
        if doctor_id and patient_id:
            appointments = await Appointment.find(And(Appointment.doctor == doctor_id, Appointment.patient == patient_id)).skip(skip).limit(limit).to_list()
        elif doctor_id:
            appointments = await Appointment.find(Appointment.doctor == doctor_id).skip(skip).limit(limit).to_list()
        elif patient_id:
            appointments = await Appointment.find(Appointment.patient == patient_id).skip(skip).limit(limit).to_list()
        else:
            appointments = await Appointment.find().skip(skip).limit(limit).to_list()
        return [AppointmentInDB(**appointment.model_dump()) for appointment in appointments]
    except DocumentNotFound:
        logger.error("No appointments found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No appointments found: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong: {e}")