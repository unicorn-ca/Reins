from unicon_pipeline_reporter.reporter import Reporter

import boto3

class CodeCommitReporter(Reporter):

    def handle(self):
        in_artifact = self.event.get_input_artifacts()[0]
        out_artifact = self.event.get_output_artifacts()[0]
        self.pass_bucket(in_artifact, out_artifact)

