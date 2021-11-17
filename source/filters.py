import logging

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from telegram.ext.filters import MessageFilter

from sending import send_info
from shelf import engine, record_table


class RecordIdFilter(MessageFilter):
    """ Is message.text an integer and correct record_id? """
    def filter(self, message):
        try:
            record_id = int(message.text)
        except ValueError:
            logging.info('Not an integer')
            return False
        count_of_records = func.count(record_table.c.id)
        stmt = select(count_of_records)
        with Session(engine) as session:
            result = session.execute(stmt)
            number_of_records = result.scalar()
        if 0 < record_id <= number_of_records:
            return True
        logging.debug('There is not such a record')
        return False


record_id_filter = RecordIdFilter()
logging.basicConfig(level=logging.INFO)
