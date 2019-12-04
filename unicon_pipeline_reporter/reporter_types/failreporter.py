from unicon_pipeline_reporter.reporter import Reporter
from code_commit_log import Log
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser


class FailReporter(Reporter):

    def handle(self):
        print("Running Auto Fail")
        self.fail("Unreconised Event")






