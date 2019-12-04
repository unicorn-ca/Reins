from unicon_pipeline_reporter.reporter import Reporter
from code_commit_log import Log
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser
from unicon_classes.IAM.root import Root as IAMRoot


class CodeCommitReporter(Reporter):

    def handle(self):
        print("Running CodeCommit")
        try:
            if self.event.get_params() is not {}:
                param = self.event.get_params()
                last_commit = Log.get_last_confirmed_commit(param['repo'], param['branch'])
                if last_commit is None:
                    raise Exception("Could Not Find Last Commit")
                check_group = IAMGroup(name=param['group'])
                compare_user = last_commit.identity
                if isinstance(compare_user, IAMRoot):
                    raise Exception("Root isn't allowed to commit to the pipeline")
                if isinstance(compare_user, IAMUser):
                    if check_group.in_group(compare_user):
                        print("PASSED TEST")
                        self.accept()
                        return
                    raise Exception("User who last commit, isn't in the valid pre-auth group")
                raise Exception("Returned User From last commit wasn't valid")
            raise Exception("Passed in param wasn't valid")
        except Exception as err:
            print("FAILED TEST")
            self.fail(errorMessage=str(err))
            raise err
        self.fail()






