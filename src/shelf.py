import os

from dotenv import load_dotenv
from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy import func, select
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session

load_dotenv()

db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True, future=True)

Base = declarative_base()

record_table = Table(
    'records',
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
    Column('record_id', ForeignKey('records.id')),
    Column('file_id', String(100)),
)


class Record(Base):
    __table__ = record_table

    tracks = relationship("Track", lazy="joined")

    def __repr__(self):
        return f'Album: {self.record_name}'
    
    @staticmethod
    def by_id(record_id: int):
        stmt = select(Record).where(Record.id == record_id)
        with Session(engine) as session:
            return session.scalar(stmt)

    @staticmethod
    def get_number_of_records():
        count_records = func.count(record_table.c.id)
        stmt = select(count_records)
        with Session(engine) as session:
            result = session.execute(stmt)
            return result.scalar()

    @staticmethod
    def get_record_list():
        stmt = select(Record)
        with Session(engine) as session:
            result = session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    def years():
        stmt = select(Record.year).group_by(Record.year)
        with Session(engine) as session:
            result = session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    def by_year(year: str):
        stmt = select(Record.id, Record.record_name).where(Record.year == year)
        with Session(engine) as session:
            result = session.execute(stmt)
            return result.all()


class Track(Base):
    __table__ = track_table

    def __repr__(self):
        return f'Track: {self.track_name}'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
