import logging
import os
from fastapi import FastAPI
from sqlmodel import SQLModel

from api.routes import appointment_routes, doctor_routes, patient_routes, prescription_routes, speciality_routes

logging.config.fileConfig(
    fname=os.path.join(os.path.dirname(__file__), "..", "logging.ini"),
    disable_existing_loggers=False
)

app = FastAPI()

app.include_router(patient_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointment_routes.router)
app.include_router(prescription_routes.router)
app.include_router(speciality_routes.router)
