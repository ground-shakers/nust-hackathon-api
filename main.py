import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models.users import Patient, Doctor, Nurse, Admin, Pharmacist
from models.appointment import Appointment
from models.treatment import Treatment
from models.medical_facilities import Hospital, Clinic
from models.pharmacy import Drug, DrugInventory, DrugManufacturer
from models.diagnosis import Diagnosis

from routers import users, patient, auth

from motor.motor_asyncio import AsyncIOMotorClient

from beanie import init_beanie

from dotenv import load_dotenv

load_dotenv()

# noinspection PyUnusedLocal,PyShadowingNames
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(os.getenv("DATABASE_CONNECTION_STRING"))  # * Connect to MongoDB

    await init_beanie(
        database=client[os.getenv("DATABASE_NAME")],
        document_models=[Patient, Doctor, Nurse, Appointment, Treatment, Hospital, Clinic, Drug, DrugInventory, DrugManufacturer, Diagnosis, Admin, Pharmacist],
    )
    yield
    client.close()
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patient.router)