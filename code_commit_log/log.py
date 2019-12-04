from cloud_trail_parser import Parser, LookupAttribute
from unicon_classes.cloud_trail import CodeCommitEvent
from datetime import datetime, timedelta
from typing import List


class Log:

    def __init__(self, start_date: datetime = None, end_date: datetime = None):
        self.start_time = datetime.now() + timedelta(5) if start_date is None else start_date
        self.end_time = datetime.now() if end_date is None else end_date

    @staticmethod
    def get_events(start_time: datetime = None, end_time: datetime = None) -> List[CodeCommitEvent]:
        if start_time is None: start_time = datetime.now() + timedelta(-30)
        if end_time is None: end_time = datetime.now()
        temp = Parser()
        events = temp.fetch([LookupAttribute(key="EventSource", value="codecommit.amazonaws.com")])
        ret: List[CodeCommitEvent] = []
        for event in events:
            if isinstance(event, CodeCommitEvent):
                ret.append(event)
        return ret

    @staticmethod
    def get_last_confirmed_commit(repo, branch, events: List[CodeCommitEvent] = None):
        if events is None:
            events = Log.get_events(start_time=datetime.now() + timedelta(hours=12))

        found: CodeCommitEvent = None

        for event in events:
            if event.event_name == "GitPush" and event.data_transferred \
                    and (found is None or found.event_time < event.event_time):
                found = event

        return found


