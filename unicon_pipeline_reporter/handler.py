from unicon_pipeline_reporter.reporter_factory import get_reporter
from pipeline_event.reporter_event_con import ReporterEvent


def handle(event, context) -> bool:
    reporter = get_reporter(ReporterEvent(event))
    return reporter.handle()
