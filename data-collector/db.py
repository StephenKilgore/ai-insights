from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from models.job import Job


def get_last_job_end_date(service_name):
    last_job = session.query(Job).filter(Job.service_name == service_name).order_by(Job.job_end_date.desc()).first()
    if last_job:
        return last_job.job_end_date
    return None
