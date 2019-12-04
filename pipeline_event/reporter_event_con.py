from pipeline_event.reporter_event import ReporterEvent as ReporterEventInst
from pipeline_event.event_con import Event


class ReporterEvent(ReporterEventInst, Event):
    def __init__(self, event: dict = None):
        super().__init__(event=event)
        self.reporter_type: str = ""
        params = self.get_params()
        if "reporterType" in params:
            self.set_reporter_type(params["reporterType"])

    def set_reporter_type(self, item):
        self.reporter_type = item

    def get_reporter_type(self):
        return self.reporter_type
