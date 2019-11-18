from pipeline_event.reporter_event import ReporterEvent
from unicon_pipeline_reporter.reporter import Reporter
from unicon_pipeline_reporter.reporter_types.codecommit import CodeCommitRepoter
from unicon_pipeline_reporter.reporter_types.fuzzerreporter import FuzzerReporter


def get_reporter(event: ReporterEvent) -> Reporter:
    if event.get_reporter_type() != "":
        if event.get_reporter_type() == "codecommit":
            return CodeCommitReporter.Reporter(event)
        if event.get_reporter_type() == "fuzzerreporter":
            return FuzzerReporter.Reporter(event)