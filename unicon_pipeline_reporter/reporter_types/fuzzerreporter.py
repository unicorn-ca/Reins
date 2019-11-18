from unicon_pipeline_reporter.reporter import Reporter
from boto3_type_annotations.lambda_ import Client

import boto3


class FuzzerReporter(Reporter):
    def handle(self):
        client:Client = boto3.client('lambda')
        # Check last modified by incorrect party
        params = {}
        params = self.event.get_params()
        response = client.get_function(
            FunctionName=params["targetLambda"]
        )
        lmf = response["LastModified"]
        # if (self.event.get_params:
            self.fail()
            exit

        # 




        #



        #

        self.accept()


