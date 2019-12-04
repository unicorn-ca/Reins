
import argparse
import json
from typing import List
from cloud_trail_parser import Parser, LookupAttribute
from code_commit_log import Log
from unicon_classes.IAM.user import User
from unicon_classes.IAM.group import Group
from unicon_classes.IAM.policy.user import UserPolicies
from pipeline_event.reporter_event_con import ReporterEvent
from index import handler
from unicon_classes.testing.lamda_context import Context

def accept():
    print("The Test Has Passed")

def failed(errorMessage,errorType):
    print("Failed Test Reason: " + errorMessage)

parser = argparse.ArgumentParser()

parser.add_argument("-ctp", "--cloudtrailparser", help="Test Cloud Parser", action="store_true")
parser.add_argument("-ccl", "--codecommitlog", help="Test CodeCommit Logs", action="store_true")
parser.add_argument("-cc2", "--codecommit2", help="Test CodeCommit Logs", action="store_true")
parser.add_argument("-ugt", "--usergrouptest", help="Test User Groups", action="store_true")
parser.add_argument("-plm", "--pipelinemapper", help="Test the mapping between Pipeline to the event", action="store_true")
parser.add_argument("-pc", "--policychecker", help="Test for overly permissive users in the account (no *)", action="store_true")
parser.add_argument("-pc2", "--policychecker2", help="Test for overly permissive users in the account (no *)", action="store_true")
parser.add_argument("-mc", "--multicheck", help="Checks Past Events for unusual activities", action="store_true")

parser.add_argument("-a", "--all", help="Run All Tests", action="store_true")

args = parser.parse_args()

# ----- CloudTrailParser ----- #

if args.cloudtrailparser or args.all:
    temp = Parser()
    events = temp.fetch([LookupAttribute(key="EventSource", value="codecommit.amazonaws.com")])
    for event in events:
        print(event.event_time, event.event_name, event.event_type)

# ----- CodeCommitLog ----- #

if args.codecommitlog or args.all:
    events = Log.get_events()
    print("----------- Testing Code Commit Log -----------")
    print("~~~~~~ Fetching Events ~~~~~~")
    for event in events:
        branch = ""
        if len(event.branches) > 0:
            branch = event.branches[0].branch
        print(event.event_time, event.event_name, event.event_type, event.repo_name, branch)
    print("~~~~~~ Fetching Last Events ~~~~~~")
    event = Log.get_last_confirmed_commit("stephen-test-pipeline", "master")
    branch = ""
    if len(event.branches) > 0:
        branch = event.branches[0].branch
    if event.identity is not None and isinstance(event.identity, User):
        event.identity.re_sync()
        print(event.identity.name, event.identity.arn, event.identity.accountID, event.identity.createDate,event.identity.passwordLastUsed)
    print(event.event_time, event.event_name, event.event_type, event.repo_name, branch, event.user_agent)
    print("----------- Finished Code Commit Log  -----------")

# ----- CodeCommitLog ----- #

if args.usergrouptest or args.all:
    print("----------- Testing User Groups -----------")
    user = User("Stephen")
    group = Group.create("StephenTestingGroup")
    if group.in_group(user):
        print("User Not In Group Test : Failed")
    else:
        print("User Not In Group Test : Passed")
    group.add_to_group(user)
    if group.in_group(user):
        print("User In Group Test : Passed")
    else:
        print("User In Group Test : Failed")
    group.delete()
    print("----------- Finished User Groups  -----------")


# ----- PipeLineMapper ----- #

if args.pipelinemapper or args.all:
    print("----------- Testing Pipeline Mapper -----------")
    exampleJson = """{
    "CodePipeline.job": {
        "id": "11111111-abcd-1111-abcd-111111abcdef",
        "accountId": "111111111111",
        "data": {
            "actionConfiguration": {
                "configuration": {
                    "FunctionName": "MyLambdaFunctionForAWSCodePipeline",
                    "UserParameters": {"reporterType":"codecommit","repo":"stephen-test-pipeline","branch":"master"}
                }
            },
            "inputArtifacts": [
                {
                    "location": {
                        "s3Location": {
                            "bucketName": "the name of the bucket configured as the pipeline artifact store in Amazon S3, for example codepipeline-us-east-2-1234567890",
                            "objectKey": "the name of the application, for example CodePipelineDemoApplication.zip"
                        },
                        "type": "S3"
                    },
                    "revision": null,
                    "name": "ArtifactName"
                }
            ],
            "outputArtifacts": [],
            "artifactCredentials": {
                "secretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                "sessionToken": "MIICiTCCAfICCQD6m7oRw0uXOjANBgkqhkiG9w0BAQUFADCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wHhcNMTEwNDI1MjA0NTIxWhcNMTIwNDI0MjA0NTIxWjCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMaK0dn+a4GmWIWJ21uUSfwfEvySWtC2XADZ4nB+BLYgVIk60CpiwsZ3G93vUEIO3IyNoH/f0wYK8m9TrDHudUZg3qX4waLG5M43q7Wgc/MbQITxOUSQv7c7ugFFDzQGBzZswY6786m86gpEIbb3OhjZnzcvQAaRHhdlQWIMm2nrAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAtCu4nUhVVxYUntneD9+h8Mg9q6q+auNKyExzyLwaxlAoo7TJHidbtS4J5iNmZgXL0FkbFFBjvSfpJIlJ00zbhNYS5f6GuoEDmFJl0ZxBHjJnyp378OD8uTs7fLvjx79LjSTbNYiytVbZPQUQ5Yaxu2jXnimvw3rrszlaEXAMPLE=",
                "accessKeyId": "AKIAIOSFODNN7EXAMPLE"
            },
            "continuationToken": "A continuation token if continuing job",
            "encryptionKey": { 
              "id": "arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab",
              "type": "KMS"
            }
        }
    }
}"""
    exampleDict = json.loads(exampleJson)
    reporter = ReporterEvent(exampleDict)
    print(reporter)

    print("----------- Finished Pipeline Mapper  -----------")

# ----- Testing Policy Checker ----- #

if args.policychecker or args.all:
    print("----------- Testing Policy Checker -----------")
    policy_group = Group('StephenTestGroup')
    users = User.get_all_users()
    errors = []
    for user in users:
        if policy_group.in_group(user=user):
            continue
        user_policy: List[UserPolicies] = user.policies
        for up_policy in user_policy:
            for statement in up_policy.statements:
                for policy, conditions in statement.actions.items():
                    if policy in ['*', 'codecommit', 's3', 'lambda']:
                        for condition in conditions:
                            if '*' in condition:
                                errors.append({'user': user.name, 'policy': policy, 'statement': condition})
    if len(errors) > 0:
        error_string = "Error, too over permissive users:\n"
        for error in errors:
            error_string = error_string + "User:{0} Policy:{1} Statement:{2}\n".format(
                error['user'], error['policy'], error['statement'])
        raise Exception(error_string)
    print("----------- Finished Policy Checker  -----------")


if args.policychecker2 or args.all:
    print("----------- Testing Policy Checker2 -----------")
    temp = Context()
    temp.function_name = "test"
    temp.aws_request_id = "2323232"
    temp_event = {
        "reporterType": "policychecker",
        "policy.access.group": "StephenTestGroup"
    }
    try:
        handler(temp_event, temp, accept, failed)
    except:
        pass
    print("----------- Finished Policy Checker  -----------")


if args.codecommit2 or args.all:
    print("----------- Testing Cloud Commit 2 -----------")
    temp = Context()
    temp.function_name = "test"
    temp.aws_request_id = "2323232"
    temp_event = {
        "reporterType": "codecommit",
        "group": "StephenTestGroup",
        "branch": "master",
        "repo": "stephen-test-pipeline"
    }
    try:
        handler(temp_event, temp, accept, failed)
    except:
        pass
    print("----------- Finished Policy Checker  -----------")


if args.multicheck or args.all:
    print("----------- Testing Cloud Commit 2 -----------")
    temp = Context()
    temp.function_name = "test"
    temp.aws_request_id = "2323232"
    temp_event = {
        "reporterType": "multichecker"
    }
    # try:
    handler(temp_event, temp, accept, failed)
    # except:
    #     pass
    print("----------- Finished Policy Checker  -----------")