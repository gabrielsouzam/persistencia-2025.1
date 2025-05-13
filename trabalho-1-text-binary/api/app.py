from fastapi import FastAPI
from api.routes import doctor_routes, patient_routes, appointment_routes

app = FastAPI()

app.include_router(doctor_routes.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(appointment_routes.router, prefix="/appointments", tags=["Appointments"])