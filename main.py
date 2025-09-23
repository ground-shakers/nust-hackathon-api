import os
import redis.asyncio as redis

from fastapi_limiter import FastAPILimiter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models.users import Patient, Doctor, Nurse, Admin, Pharmacist
from models.appointment import Appointment
from models.treatment import Treatment
from models.medical_facilities import Hospital, Clinic
from models.pharmacy import Drug, DrugInventory, DrugManufacturer
from models.diagnosis import Diagnosis

from middleware.idempotency import IdempotencyMiddleware

from routers import doctor, patient, auth

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
    
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_connection = redis.from_url(
        redis_url, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_connection)
    
    yield
    client.close()
    await redis_connection.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    IdempotencyMiddleware,
    ttl_seconds=3600,
    lock_ttl=10,
)

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)