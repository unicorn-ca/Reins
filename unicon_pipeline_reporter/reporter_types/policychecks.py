from unicon_pipeline_reporter.reporter import Reporter
from code_commit_log import Log
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser


class CodeCommitReporter(Reporter):

    def handle(self):
        print("Running CodeCommit")
        try:
            if self.event.get_params() is not {}:
                param = self.event.get_params()

            raise Exception("Passed in param wasn't valid")
        except Exception as err:
            print("FAILED TEST")
            self.fail(errorMessage=str(err))
            raise err
        self.fail()






