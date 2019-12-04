import unicon_pipeline_reporter.handler as upr_handler
from typing import Callable


def handler(event, context,
           accept: Callable[[object], None] = None,
           fail: Callable[[object, str, str], None] = None):
    upr_handler.handle(event, context, accept, fail)
