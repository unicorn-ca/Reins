from unicon_pipeline_reporter.reporter import Reporter
from code_commit_log import Log


class CodeCommitReporter(Reporter):

    def handle(self):
        in_artifact = self.event.get_input_artifacts()[0]
        out_artifact = self.event.get_output_artifacts()[0]
        self.pass_bucket(in_artifact, out_artifact)
        if self.event.get_params() is not "":

        last_commit = Log.get_last_confirmed_commit()



