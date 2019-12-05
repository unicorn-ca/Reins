from unicon_pipeline_reporter.reporter_factory import get_reporter
from pipeline_event.reporter_event_con import ReporterEvent
from typing import Callable
import boto3
from boto3_type_annotations.sns import Client


def push_to_sns(error_message, error_type, topic_arn):
    snsclient: Client = boto3. client('sns')
    print(error_message, topic_arn)
    snsclient.publish(Message=error_message, TopicArn=topic_arn)


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
        reporter = get_reporter(temp)

    if accept is not None:
        if 'accept_sns_arn' in event:
            reporter.set_accept(lambda: (accept() , push_to_sns("Job: {0} Was Accepted".format(reporter.event.get_id()),
                                                               "", event['accept_sns_arn'])))
        else:
            reporter.set_accept(accept)
    elif 'accept_sns_arn' in event:
        reporter.set_accept(lambda: push_to_sns("Job: {0} Was Accepted".format(reporter.event.get_id()), "", event['accept_sns_arn']))

    if fail is not None:
        if 'fail_sns_arn' in event:
            reporter.set_fail(lambda message, error_type: (fail(message, error_type) , push_to_sns(message, error_type, event['fail_sns_arn'])))
        else:
            reporter.set_fail(fail)
    elif 'fail_sns_arn' in event:
        reporter.set_fail(lambda message, error_type: push_to_sns(message, error_type, event['fail_sns_arn']))

    return reporter.handle()

