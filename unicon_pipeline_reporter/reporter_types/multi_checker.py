from unicon_pipeline_reporter.reporter import Reporter
from cloud_trail_parser.parser import Parser, LookupAttribute
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser
from datetime import datetime, timedelta


class MultiCheckerReporter(Reporter):

    def handle(self):
        print("Running MultiChecker")
        try:
            if self.event.get_params() is not {}:
                param = self.event.get_params()
                parse = Parser()
                events = parse.fetch(
                    # lookup_attributes=[
                    #     LookupAttribute(key="EventSource", value="codecommit.amazonaws.com"),
                    #     LookupAttribute(key="EventSource", value="s3.amazonaws.com"),
                    #     LookupAttribute(key="EventSource", value="codepipeline.amazonaws.com"),
                    #     LookupAttribute(key="EventSource", value="lambda.amazonaws.com")
                    # ],
                    start_time=datetime.now() + timedelta(hours=-12)
                )
                for event in events:
                    print("EventSource: {0} EventName: {1} EventType: {2} UserName: {3}".format(event.event_source,
                                                                                  event.event_name,
                                                                                  event.event_type,event.username)
                          )
                self.accept()
                return

            raise Exception("Passed in param wasn't valid")
        except Exception as err:
            print("FAILED TEST")
            self.fail(errorMessage=str(err))
            raise err
        self.fail()






