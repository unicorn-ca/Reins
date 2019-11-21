from unicon_pipeline_reporter.reporter import Reporter
from code_commit_log import Log
from unicon_classes.IAM import IAMGroup, IAMUser


class CodeCommitReporter(Reporter):

    def handle(self):
        in_artifact = self.event.get_input_artifacts()[0]
        out_artifact = self.event.get_output_artifacts()[0]
        self.pass_bucket(in_artifact, out_artifact)
        group = "StephenTestGroup"
        if self.event.get_params() is not "":
            last_commit = Log.get_last_confirmed_commit('stephen-test-pipeline', 'master')
            if last_commit is None:
                raise Exception("Could Not Find Last Commit")
            check_group = IAMGroup(name=group)
            compare_user = last_commit.user_agent
            if isinstance(compare_user, IAMUser):
                if check_group.in_group(compare_user):
                    self.accept()
                    return
        self.fail()






