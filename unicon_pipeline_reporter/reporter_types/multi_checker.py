from unicon_pipeline_reporter.reporter import Reporter
from cloud_trail_parser.parser import Parser, LookupAttribute
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser
from unicon_classes.IAM.root import Root as IAMRoot
from unicon_classes.cloud_trail.event_decode import BasicDecode as Event
from unicon_classes.cloud_trail.code_pipeline import CodePipeline as CTCodePipeline
from unicon_classes.cloud_trail.lambda_event import Lambda as LambdaEvents
from unicon_classes.cloud_trail.s3_event import AWSS3Event
from datetime import datetime, timedelta


class MultiCheckerReporter(Reporter):

    def handle(self):
        print("Running MultiChecker")
        try:
            if self.event.get_params() is not {}:
                param = self.event.get_params()
                if 'group' not in param:
                    raise Exception('Group Parameter is Missing')

                SuperGroup = IAMGroup(param['group'])

                parse = Parser()
                events = parse.fetch(
                    lookup_attributes=[
                        LookupAttribute(key="EventSource", value="codecommit.amazonaws.com"),
                        LookupAttribute(key="EventSource", value="s3.amazonaws.com"),
                        LookupAttribute(key="EventSource", value="codepipeline.amazonaws.com"),
                        LookupAttribute(key="EventSource", value="lambda.amazonaws.com")
                    ],
                    start_time=datetime.now() + timedelta(hours=-15)
                )
                errors = []
                for event in events:
                    if isinstance(event, Event):
                        if isinstance(event.identity, IAMRoot):
                            errors.append({'message': 'IAM Root Was Active', 'event': event})
                            continue
                        if isinstance(event.identity, IAMUser) and SuperGroup.in_group(event.identity):
                            continue
                        if isinstance(event, CTCodePipeline):
                            if isinstance(event.identity, IAMUser) and event.event_name in\
                                    [
                                        "UpdatePipeline",
                                        "DeletePipeline",
                                        "DisableStageTransition",
                                        "DeleteWebhook",
                                        "PutJobFailureResult",
                                        'EnableStageTransition'
                                    ]:
                                errors.append({'message': 'A Non-authorised User Used {0} on a pipeline'.format(
                                    event.event_name), 'event': event})

                        if isinstance(event, LambdaEvents):
                            if isinstance(event.identity, IAMUser) and event.event_name in\
                                    [
                                        "DeleteFunction",
                                        "UpdateFunctionCode",
                                        "DeleteWebhook",
                                        "UpdateFunctionConfiguration",
                                        'UpdateEventSourceMapping',
                                        "DeleteEventSourceMapping",
                                        "RemovePermission",
                                        "AddPermission",
                                        "RemoveLayerVersionPermission"
                                    ]:
                                errors.append({'message': 'A Non-authorised User Used {0} on a Lambda Function'.format(
                                    event.event_name), 'event': event})

                        if isinstance(event, AWSS3Event):
                            if isinstance(event.identity, IAMUser) and event.event_name in\
                                    [
                                        "DeleteBucket",
                                        "PutObject",
                                        "ReplicateDelete",
                                        "PutEncryptionConfiguration",
                                        'DeleteObject',
                                        "DeleteObjectVersion",
                                        "PutBucketLogging",
                                        "PutBucketObjectLockConfiguration",
                                        "PutBucketVersioning",
                                        "PutBucketPublicAccessBlock",
                                        "ObjectOwnerOverrideToBucketOwner",
                                        "PutBucketPolicy",
                                        "DeleteBucketPolicy"
                                    ]:
                                errors.append({'message': 'A Non-authorised User Used {0} on a Lambda Function'.format(
                                    event.event_name), 'event': event})

                if len(errors) > 0:
                    error_message = "FAILED MultiChecker for the following reasons:\n"
                    for error in errors:
                        error_message = error_message + "Time: {0} EventSource : {2} EventName: {3} " \
                                                        "Username: {4} Reason: {1}\n".format(error['event'].event_time,
                                                                                           error['message'],
                                                                                           error['event'].event_source,
                                                                                           error['event'].event_name,
                                                                                           error['event'].username)
                    raise Exception(error_message)
                print("PASSED")
                self.accept()
                return

            raise Exception("Passed in param wasn't valid")
        except Exception as err:
            print("FAILED TEST")
            self.fail(errorMessage=str(err))
            raise err
        self.fail()






 # print("Time: {4} EventSource: {0} EventName: {1} EventType: {2} UserName: {3}".format(event.event_source,
 #                                                                                  event.event_name,
 #                                                                                  event.event_type,
 #                                                                                  event.username,
 #                                                                                  event.event_time)
 #                          )