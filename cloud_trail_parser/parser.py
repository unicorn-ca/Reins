from unicon_classes.cloud_trail import EventFactory,Event
from typing import List, Callable
from datetime import datetime, timedelta
import time
import boto3
from boto3_type_annotations.cloudtrail import Client


class LookupAttribute:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def to_dict(self, prefix: str = "Attribute", postfix: str = ""):
        return {
            prefix + "Key" + postfix : self.key,
            prefix + "Value" + postfix : self.value
        }


class Parser:

    def __init__(self):
        self.cloud_trail: Client = boto3.client('cloudtrail')

    @staticmethod
    def __sort(events: List[Event]) -> List[Event]:
        return sorted(events, key=lambda event: event.event_time, reverse=True)

    def fetch(self, lookup_attributes: List[LookupAttribute] = None, start_time: datetime = None,
              end_time: datetime = None, finish_func: Callable[[Event], bool] = None) -> List[Event]:
        if lookup_attributes is None: lookup_attributes = []
        if start_time is None: start_time = datetime.now() + timedelta(-30)
        if end_time is None: end_time = datetime.now()

        lookup_attributes_convert = list(map(lambda x: x.to_dict(), lookup_attributes))

        events: List[Event] = []
        prev_time = datetime.now()
        for index, lookup_attributes_convert_single in enumerate(lookup_attributes_convert):
            # gets a accuret
            wait_time = datetime.now() - (prev_time + timedelta(seconds=0.5))
            wait_time = wait_time.total_seconds()
            if index > 0 and wait_time < 0:
                time.sleep(wait_time * -1)

            next_token_flag = True
            next_token = ""
            while next_token_flag:
                next_token_flag = False
                if next_token == "":
                    response = self.cloud_trail.lookup_events(
                        LookupAttributes=[lookup_attributes_convert_single],
                        StartTime=start_time,
                        EndTime=end_time
                    )
                else:
                    response = self.cloud_trail.lookup_events(
                        LookupAttributes=[lookup_attributes_convert_single],
                        StartTime=start_time,
                        EndTime=end_time,
                        NextToken=next_token
                    )
                prev_time = datetime.now()
                for name, item in response.items():
                    if name == 'NextToken':
                        next_token_flag = True
                        next_token = item
                    elif name == "Events":
                        for event in item:
                            temp = EventFactory.create(event)
                            events.append(temp)
                            if finish_func is not None:
                                if finish_func(temp):
                                    return self.__sort(events)
                if next_token_flag:
                    # time.sleep(1)
                    pass
        return self.__sort(events)
