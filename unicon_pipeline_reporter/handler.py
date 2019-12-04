from unicon_pipeline_reporter.reporter_factory import get_reporter
from pipeline_event.reporter_event_con import ReporterEvent
from typing import Callable


def handle(event, context,
           accept: Callable[[object], None] = None,
           fail: Callable[[object, str, str], None] = None) -> bool:
    if 'CodePipeline.job' in event:
        reporter = get_reporter(ReporterEvent(event))
    else:
        if 'reporterType' not in event:
            raise Exception('Missing ReporterType in paramater ')
        temp = ReporterEvent()
        temp.set_params(event)
        temp.set_lambda_name(context.function_name)
        temp.set_id(context.aws_request_id)
        temp.set_reporter_type(event['reporterType'])
        reporter = get_reporter(ReporterEvent(event))
    if accept is not None:
        reporter.set_accept(accept)
    if fail is not None:
        reporter.set_fail(fail)

    return reporter.handle()

