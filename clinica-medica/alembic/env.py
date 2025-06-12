import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool
from dotenv import load_dotenv
from alembic import context
from sqlmodel import SQLModel

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importar apenas o necessário no escopo global
target_metadata = SQLModel.metadata

def get_url():
    return DATABASE_URL

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    
    # Importar os modelos APÓS a configuração inicial
    # Isso evita problemas de importação circular
    from api.models.appointment import Appointment
    from api.models.doctor import Doctor
    from api.models.patient import Patient
    from api.models.prescription import Prescription
    from api.models.specialty import Specialty
    
    # Garante que todos os modelos estão registrados
    for model in [Appointment, Doctor, Patient, Prescription, Specialty]:
        model.update_forward_refs()
    
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()