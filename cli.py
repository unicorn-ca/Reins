import argparse
import json
from index import handler
from unicon_classes.testing.lamda_context import Context


def accept():
    print("TEST HAS PASSED")


def failed(errorMessage, errorType):
    print("TEST HAS FAILED Reason: " + errorMessage)


parser = argparse.ArgumentParser()
parser.add_argument("checker", help="The Name of the checker")
parser.add_argument("jsonparam", help="User params as a json object")


args = parser.parse_args()

print("----------- Running {0} -----------".format(args.checker))
temp = Context()
temp.function_name = "cli-checker"
temp.aws_request_id = "2323232"
event = {}
try:
    event = json.loads(args.jsonparam)
except Exception as e:
    print("JSON encoded failed: {0}".format(str(e)))
    exit(-1)

event["reporterType"] = args.checker
handler(event, temp, accept, failed)

print("----------- Finished {0} -----------".format(args.checker))

