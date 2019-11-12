from pipeline_event.reporter_event import ReporterEvent
from pipeline_event.artifacts import Artifacts
from abc import ABC, abstractmethod
from boto3_type_annotations import cloudformation, codepipeline


import boto3


class Reporter:

    def __init__(self, event: ReporterEvent):
        self.event: ReporterEvent = event
        self.cf: cloudformation.Client = boto3.client('cloudformation')
        self.cp: codepipeline.Client = boto3.client('codepipeline')

    @abstractmethod
    def handle(self):
        pass

    def pass_bucket(self, in_artifact: Artifacts, out_artifact: Artifacts):
        in_artifact.copy_to(out_artifact)

    def accept(self):
        self.cp.put_job_success_result(jobId=self.event.get_id())

    def fail(self):
        self.cp.put_job_failure_result(jobId=self.event.get_id())
