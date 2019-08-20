import os
import logging

from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2.types import Geography
from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func

HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]
PORT = os.environ["PORT"]


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


Base = declarative_base()
Session = sessionmaker()
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, HOST, DB_PORT, DB_NAME))

# session.execute(select([func.InitSpatialMetaData()]))

Base.metadata.create_all(engine)

Session.configure(bind=engine)

listen(engine, 'connect', load_spatialite)

session = Session()

class Apartment(Base):

    __tablename__ = 'apartments'

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
    latLng = Column(Geography(geometry_type='POINT', srid=4326, ))
