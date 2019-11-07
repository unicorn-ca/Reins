import unicon_pipeline_reporter.handler as upr_handler


def handler(event, context):
    upr_handler.handle(event, context)
