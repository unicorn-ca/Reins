from pipeline_event.reporter_event import ReporterEvent
from unicon_pipeline_reporter.reporter import Reporter


def get_reporter(event :ReporterEvent) -> Reporter:
    if event.get_reporter_type() != "":
