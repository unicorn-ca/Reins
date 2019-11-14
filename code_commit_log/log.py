from cloud_trail_parser import Parser, LookupAttribute
from datetime import datetime, timedelta
from typing import List

class Log:
    def __init__(self, start_date: datetime = None, end_date: datetime = None):
        self.start_time = datetime.now() + timedelta(5) if start_date is None else start_date
        self.end_time = datetime.now() if end_date is None else end_date

    @staticmethod
    def get_events(start_time: datetime = None, end_time: datetime = None):
        if start_time is None: start_time = datetime.now() + timedelta(-30)
        if end_time is None: end_time = datetime.now()