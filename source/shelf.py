import os

from dotenv import load_dotenv
from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship

load_dotenv()

db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True, future=True)

Base = declarative_base()


""" ##########TABLES########## """


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


""" ##########MODELS########## """


class Record(Base):
    __table__ = record_table

    tracks = relationship("Track")

    def __repr__(self):
        return f'Album: {self.record_name}'


class Track(Base):
    __table__ = track_table

    def __repr__(self):
        return f'Track: {self.track_name}'


""" #########POPULATE######### """


if __name__ == '__main__':
    Base.metadata.create_all(engine)
