import os
import logging

from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2.types import Geography
from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]
PORT = os.environ["PORT"]

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()
Session = sessionmaker()

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, HOST, DB_PORT, DB_NAME))

class Apartment(Base):

    __tablename__ = 'listings'

    id = Column(UUID, primary_key=True, default=uuid4)
    no_bed = Column(Integer)
    no_bath = Column(Integer)
    no_toilets = Column(Integer)
    price = Column(Float)
    url = Column(String)
    address = Column(String)
    description = Column(String)
    source = Column(String)
    date_added = Column(Date)
    latlng = Column(Geography(geometry_type='POINT', srid=4326))


if not engine.dialect.has_table(engine, 'listings'):
    Apartment.__table__.create(engine)
