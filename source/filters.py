import logging

from telegram.ext.filters import MessageFilter

import shelf


class RecordIdFilter(MessageFilter):
    """ Is message.text an integer and correct record_id? """
    def filter(self, message):
        try:
            record_id = int(message.text)
        except ValueError:
            logging.info('Not an integer')
            return False
        number_of_records = shelf.count_records()
        if 0 < record_id <= number_of_records:
            return True
        logging.info('There is not such a record')
        return False


record_id_filter = RecordIdFilter()
logging.basicConfig(level=logging.INFO)
