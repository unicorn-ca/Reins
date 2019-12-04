import json
from cloud_trail_parser import Parser, LookupAttribute
from code_commit_log import Log
from unicon_classes.IAM.user import User
from unicon_classes.IAM.group import Group
from pipeline_event.reporter_event_con import ReporterEvent

from index import handler
from unicon_classes.testing.lamda_context import Context


# ----- CloudTrailParser ----- #

def cloudtrailparser():
    temp = Parser()
    events = temp.fetch([LookupAttribute(key="EventSource", value="codecommit.amazonaws.com")])
    for event in events:
        print(event.event_time, event.event_name, event.event_type)

# ----- CodeCommitLog ----- #

def codecommitlog(repo,in_branch):
    events = Log.get_events()
    print("----------- Testing Code Commit Log -----------")
    print("~~~~~~ Fetching Events ~~~~~~")
    for event in events:
        branch = ""
        if len(event.branches) > 0:
            branch = event.branches[0].branch
        print(event.event_time, event.event_name, event.event_type, event.repo_name, branch)
    print("~~~~~~ Fetching Last Events ~~~~~~")
    event = Log.get_last_confirmed_commit(repo, in_branch)
    branch = ""
    if len(event.branches) > 0:
        branch = event.branches[0].branch
    if event.identity is not None and isinstance(event.identity, User):
        event.identity.re_sync()
        print(event.identity.name, event.identity.arn, event.identity.accountID, event.identity.createDate,event.identity.passwordLastUsed)
    print(event.event_time, event.event_name, event.event_type, event.repo_name, branch, event.user_agent)
    print("----------- Finished Code Commit Log  -----------")

# ----- CodeCommitLog ----- #

def CodeCommitLog(in_user):
    print("----------- Testing User Groups -----------")
    user = User(in_user)
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

# ----- CodeCommitLog ----- #

def last_user_commit(repo, in_branch, in_group):
    print("----------- Testing last_user_commit -----------")
    event = Log.get_last_confirmed_commit(repo, in_branch)
    group = Group(in_group)
    if group.in_group(event.identity):
        print("User In Group")
    else:
        print("User Not In Group")
    print("----------- Finished last_user_commit  -----------")

def CodeCommitLogInGroup(in_user,in_group):
    print("----------- Testing User Groups -----------")
    user = User(in_user)
    group = Group(in_group)
    if group.in_group(user):
        print("User In Group Test")
    else:
        print("User Not In Group Test")
    print("----------- Finished User Groups  -----------")

def handler(event, context):
    reporter = ReporterEvent(event)
    print(reporter)
    # cloudtrailparser()
    params = reporter.get_params()
    # codecommitlog(params['repo'], params['branch'])
    last_user_commit(params['repo'], params['branch'],  params['group'])
