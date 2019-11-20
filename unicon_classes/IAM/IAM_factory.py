from unicon_classes.IAM import IAMUser, IAMBasic, IAMGroup


class IAMFactory:

    @staticmethod
    def create( user: dict) -> IAMBasic:
        iam: IAMBasic = IAMBasic()
        if user['type'] == "IAMUser":
            iam: IAMUser = IAMUser()
            for name, item in user.items():
                if name == "accessKeyId": iam.accessKeyId = item
                if name == "userName": iam.name = item

        elif user['type'] == "IAMGroup":
            iam: IAMGroup = IAMGroup()

        for name, item in user.items():
            if name == "principalId": iam.principalId = item
            if name == "arn": iam.arn = item
            if name == "accountId": iam.accountID = item

        return iam
