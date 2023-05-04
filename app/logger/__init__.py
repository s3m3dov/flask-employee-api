import logging


class Formatter(logging.Formatter):
    def format(self, record):
        record.worker_id = "request.uuid"  # replace this with your variable
        return super(Formatter, self).format(record)
