from pipeline_event.reporter_event import ReporterEvent
from unicon_pipeline_reporter.reporter import Reporter
from unicon_pipeline_reporter.reporter_types import codecommit


def get_reporter(event: ReporterEvent) -> Reporter:
    if event.get_reporter_type() != "":
        if event.get_reporter_type() == "codecommit":
            return codecommit.CodeCommitReporter(event)
