from unicon_classes.cloud_trail import Event, CodeCommitEvent, S3Event, CodePipelineEvent, LambdaEvent


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
            else:
                return Event(event)
        raise Exception("The Event Input doesn't have a EventSource")
