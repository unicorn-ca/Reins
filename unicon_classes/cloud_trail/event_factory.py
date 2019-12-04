from unicon_classes.cloud_trail import Event, CodeCommitEvent
from unicon_classes.cloud_trail.code_pipeline import CodePipeline as CodePipelineEvent
from unicon_classes.cloud_trail.lambda_event import Lambda as LambdaEvent
from unicon_classes.cloud_trail.s3_event import AWSS3Event as S3Event
from unicon_classes.cloud_trail.iam import IAM as IAMEvent
from unicon_classes.cloud_trail.sts import STS as STSEvent
from unicon_classes.cloud_trail.kms import KMS as KMSEvent
from unicon_classes.cloud_trail.signin import SignIn as SignInEvent


class EventFactory:

    def create(event:dict)-> Event:
        if 'EventSource' in event:
            if event['EventSource'] == "codecommit.amazonaws.com":
                return CodeCommitEvent(event)
            if event['EventSource'] == "s3.amazonaws.com":
                return S3Event(event)
            if event['EventSource'] == "codepipeline.amazonaws.com":
                return CodePipelineEvent(event)
            if event['EventSource'] == "lambda.amazonaws.com":
                return LambdaEvent(event)
            if event['EventSource'] == "iam.amazonaws.com":
                return IAMEvent(event)
            if event['EventSource'] == "kms.amazonaws.com":
                return KMSEvent(event)
            if event['EventSource'] == "sts.amazonaws.com":
                return STSEvent(event)
            if event['EventSource'] == "signin.amazonaws.com":
                return SignInEvent(event)
            else:
                return Event(event)
        raise Exception("The Event Input doesn't have a EventSource")
