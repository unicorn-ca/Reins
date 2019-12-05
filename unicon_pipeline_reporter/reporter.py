from pipeline_event.reporter_event import ReporterEvent
from pipeline_event.artifacts import Artifacts
from abc import ABC, abstractmethod
from typing import Callable
from boto3_type_annotations import cloudformation, codepipeline,sns


import boto3


class Reporter:

    def __init__(self, event: ReporterEvent):
        self.event: ReporterEvent = event
        self.cf: cloudformation.Client = boto3.client('cloudformation')
        self.cp: codepipeline.Client = boto3.client('codepipeline')
        self.__accept = None
        self.__fail = None

    def __push_to_sns(self, error_message, error_type, topic_arn):
        snsclient: sns.Client = boto3.client('sns')
        print(error_message, topic_arn)
        snsclient.publish(Message=error_message, TopicArn=topic_arn)

    def set_accept(self, accept: Callable[[object], None]):
        self.__accept = accept

    def set_fail(self, fail: Callable[[object,str,str], None]):
        self.__fail = fail

    def set_fail_default(self):
        self.__fail = None

    def set_accept_default(self):
        self.__accept = None

    @abstractmethod
    def handle(self):
        pass

    def pass_bucket(self, in_artifact: Artifacts, out_artifact: Artifacts):
        in_artifact.copy_to(out_artifact)

    def accept(self):
        if 'accept_sns_arn' in self.event.get_params():
            self.__push_to_sns("Job: {0} Was Accepted".format(self.event.get_id()),"", self.event.get_params()['accept_sns_arn'])
        if self.__accept is not None:
            self.__accept()
        else:
            self.cp.put_job_success_result(jobId=self.event.get_id())

    def fail(self, errorMessage="GenericErrorMessage", errorType="JobFailed"):
        if 'fail_sns_arn' in self.event.get_params():
            self.__push_to_sns(errorMessage, errorType, self.event.get_params()['fail_sns_arn'])
        if self.__fail is not None:
            self.__fail(errorMessage, errorType)
        else:
            self.cp.put_job_failure_result(jobId=self.event.get_id(), failureDetails={
                'type': errorType,
                'message': errorMessage
            })
