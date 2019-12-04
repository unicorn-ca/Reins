from pipeline_event.reporter_event import ReporterEvent
from unicon_pipeline_reporter.reporter import Reporter
from unicon_pipeline_reporter.reporter_types import codecommit
from unicon_pipeline_reporter.reporter_types import policychecks
from unicon_pipeline_reporter.reporter_types import passreport
from unicon_pipeline_reporter.reporter_types import failreporter
from unicon_pipeline_reporter.reporter_types import multi_checker


def get_reporter(event: ReporterEvent) -> Reporter:
    if event.get_reporter_type() != "":
        if event.get_reporter_type() == "codecommit":
            return codecommit.CodeCommitReporter(event)
        if event.get_reporter_type() == "policychecker":
            return policychecks.PolicyCheckerReporter(event)
        if event.get_reporter_type() == "multichecker":
            return multi_checker.MultiCheckerReporter(event)
        if event.get_reporter_type() == "pass":
            return passreport.PassReporter(event)
    return failreporter.FailReporter(event)
