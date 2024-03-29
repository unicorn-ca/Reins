from abc import ABC, abstractmethod
from pipeline_event.event import Event


class ReporterEvent(Event):

    @abstractmethod
    def get_reporter_type(self):
        pass

    @abstractmethod
    def set_reporter_type(self, item):
        pass

    def __str__(self):
        ret = super().__str__()
        return ret + """
Reporter Type = {0}""".format(self.get_reporter_type())
