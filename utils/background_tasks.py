"""
Background tasks for the application.
"""

from .notification import send_sms_notification

from .api_logger import logger

from models.appointment import Appointment
from models.users import Patient, Doctor
from beanie import PydanticObjectId

async def notify_appointment_creation(appointment: Appointment):
    """Notify patient and doctor about the appointment creation via SMS.

    Args:
        patient_id (str): The patient's ID.
        doctor_id (str): The doctor's ID.
        appointment_id (str): The appointment ID.
    """
    patient_in_db = await Patient.get(PydanticObjectId(appointment.patient))
    doctor_in_db = await Doctor.get(PydanticObjectId(appointment.doctor))
    appointment_in_db = await Appointment.get(PydanticObjectId(appointment.id))

    if not patient_in_db:
        logger.error(f"Patient with ID {appointment.patient} not found.")
        return

    if not appointment_in_db:
        logger.error(f"Appointment with ID {appointment.id} not found.")
        return

    patient_message = f"Your appointment has been scheduled for {appointment_in_db.appointment_date} with {doctor_in_db.first_name} {doctor_in_db.last_name}. Appointment ID: {appointment_in_db.id}"
    
    doctor_message = f"""
    You have a new appointment scheduled for {appointment_in_db.appointment_date} with patient {patient_in_db.first_name} {patient_in_db.last_name}. Appointment ID: {appointment_in_db.id}
    """

    send_sms_notification(to=patient_in_db.contact_info.phone, message=patient_message)
    send_sms_notification(to=doctor_in_db.contact_info.phone, message=doctor_message)