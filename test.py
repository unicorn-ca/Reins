
import argparse
from cloud_trail_parser import Parser, LookupAttribute
from code_commit_log import Log
from unicon_classes.IAM.user import User
from unicon_classes.IAM.group import Group

parser = argparse.ArgumentParser()

parser.add_argument("-ctp", "--cloudtrailparser", help="Test Cloud Parser", action="store_true")
parser.add_argument("-ccl", "--codecommitlog", help="Test CodeCommit Logs", action="store_true")
parser.add_argument("-ugt", "--usergrouptest", help="Test User Groups Intrations", action="store_true")

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
    user = User("arn:aws:iam::485183173290:user/Stephen")


    events = Log.get_events()
    print("----------- Testing User Groups -----------")
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
        print(event.identity.name, event.identity.accountID, event.identity.createDate,event.identity.passwordLastUsed)
    print(event.event_time, event.event_name, event.event_type, event.repo_name, branch, event.user_agent)
    print("----------- Finished  -----------")