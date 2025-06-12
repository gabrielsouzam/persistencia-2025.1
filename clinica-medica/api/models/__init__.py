from .patient import Patient, PatientCreate, PatientRead
from .doctor import Doctor, DoctorCreate, DoctorRead
from .specialty import Specialty, SpecialtyCreate, SpecialtyRead
from .appointment import Appointment, AppointmentCreate, AppointmentRead
from .prescription import Prescription, PrescriptionCreate, PrescriptionRead

__all__ = [
    'Patient', 'PatientCreate', 'PatientRead',
    'Doctor', 'DoctorCreate', 'DoctorRead',
    'Specialty', 'SpecialtyCreate', 'SpecialtyRead',
    'Appointment', 'AppointmentCreate', 'AppointmentRead',
    'Prescription', 'PrescriptionCreate', 'PrescriptionRead'
]