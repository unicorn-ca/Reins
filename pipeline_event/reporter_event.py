from abc import ABC, abstractmethod
from pipeline_event.event import Event


class ReporterEvent(Event):

    @abstractmethod
    def get_reporter_type(self):
        pass

    @abstractmethod
    def set_reporter_type(self, item):
        pass
