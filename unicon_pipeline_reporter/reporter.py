from pipeline_event.reporter_event import ReporterEvent
from pipeline_event.artifacts import Artifacts
from abc import ABC, abstractmethod
from typing import Callable
from boto3_type_annotations import cloudformation, codepipeline


import boto3


class Reporter:

    def __init__(self, event: ReporterEvent):
        self.event: ReporterEvent = event
        self.cf: cloudformation.Client = boto3.client('cloudformation')
        self.cp: codepipeline.Client = boto3.client('codepipeline')
        self.__accept = None
        self.__fail = None

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
        if self.__accept is not None:
            self.__accept(self)
        else:
            self.cp.put_job_success_result(jobId=self.event.get_id())

    def fail(self, errorMessage="GenericErrorMessage", errorType="JobFailed"):
        if self.__fail is not None:
            self.__fail(self, errorMessage, errorType)
        else:
            self.cp.put_job_failure_result(jobId=self.event.get_id(), failureDetails={
                'type': errorType,
                'message': errorMessage
            })
