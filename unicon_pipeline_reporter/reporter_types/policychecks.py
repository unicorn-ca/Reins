from unicon_pipeline_reporter.reporter import Reporter
from unicon_classes.IAM.group import Group as IAMGroup
from unicon_classes.IAM.user import User as IAMUser
from unicon_classes.IAM.policy.user import UserPolicies
from typing import List


class PolicyCheckerReporter(Reporter):

    def handle(self):
        print("Running PolicyChecker")
        try:
            if self.event.get_params() is not {}:
                param = self.event.get_params()
                if 'group' not in param:
                    raise Exception("PolicyChecker Needs A Master 'Group'")
                policy_group_name = param['group']
                policy_group = IAMGroup(policy_group_name)
                users = IAMUser.get_all_users()
                errors = []
                for user in users:
                    if policy_group.in_group(user=user):
                        continue
                    user_policy: List[UserPolicies] = user.policies
                    for up_policy in user_policy:
                        for statement in up_policy.statements:
                            for policy, conditions in statement.actions.items():
                                if policy in ['*', 'codecommit', 's3', 'lambda', 'codepipeline']:
                                    for condition in conditions:
                                        if '*' in condition or 'Put' in condition or 'Delete' in \
                                                condition or 'Update' in condition or 'Disable' in condition:
                                            errors.append({'user': user.name, 'policy': policy, 'statement': condition})
                if len(errors) > 0:
                    error_string = "Error, too over permissive users:\n"
                    for error in errors:
                        error_string = error_string + "User:{0} Policy:{1} Statement:{2}\n".format(
                            error['user'], error['policy'], error['statement'])
                    raise Exception(error_string)
                self.accept()
                return
            else:
                raise Exception("Passed in param wasn't valid")
        except Exception as err:
            print("FAILED TEST")
            self.fail(errorMessage=str(err))
            raise err
        self.fail()






