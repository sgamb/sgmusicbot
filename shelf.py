import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base


db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True, future=True)

Base = declarative_base()

record_table = Table(
    'record_collection',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('record_name', String),
    Column('year', String(10)),
)

track_table = Table(
    'tracks',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('track_name', String),
    Column('record_id', ForeignKey('record_collection.id')),
    Column('file_id', String(100)),
)


class Record(Base):
    __table__ = record_table

    def __repr__(self):
        return f'Album: {self.record_name}'


class Track(Base):
    __table__ = track_table

    def __repr__(self):
        return f'Track: {self.track_name}'


Base.metadata.create_all(engine)
