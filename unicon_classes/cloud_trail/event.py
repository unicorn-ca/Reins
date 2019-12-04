from datetime import datetime
from typing import List
import json


class EventResources:
    def __init__(self, resource: dict):
        self.name = ""
        self.type = ""
        self.__convert(resource)

    def __convert(self, resource: dict):
        for name, item in resource.items():
            if name == "ResourceType": self.type = item
            if name == "ResourceName": self.name = name


class Event:
    def __init__(self, event: dict, json_decode_cloud_trail_event: bool = False):
        self.event_type = ""
        self.event_ID = ""
        self.event_name = ""
        self.read_only = ""
        self.access_key_id = ""
        self.event_time = datetime.now()
        self.event_source = ""
        self.username = ""
        self.resources: List[EventResources] = []
        self.cloud_trail_event = ""
        self.__convert(event, json_decode_cloud_trail_event)


    def __convert(self, event: dict, json_decode_cloud_trail_event: bool = False):
        for name, item in event.items():
            if name == 'EventId' : self.event_ID = item
            if name == 'EventName' : self.event_name = item
            if name == 'ReadOnly': self.read_only = item
            if name == 'AccessKeyId' : self.access_key_id = item
            if name == 'EventTime': self.event_time = item
            if name == 'EventSource': self.event_source = item
            if name == 'Username': self.username = item
            if name == 'CloudTrailEvent':
                if json_decode_cloud_trail_event:
                    self.cloud_trail_event = json.loads(item)
                else:
                    self.cloud_trail_event = item
            if name == "Resources":
                for resource in item:
                    self.resources.append(EventResources(resource))



