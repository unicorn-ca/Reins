from unicon_classes.IAM.user import User
from unicon_classes.IAM.base import Base
from unicon_classes.IAM.group import Group



class IAMFactory:

    @staticmethod
    def create( user: dict) -> Base:
        iam: Base = Base()
        if user['type'] == "IAMUser":
            iam: User = User()
            for name, item in user.items():
                if name == "accessKeyId": iam.accessKeyId = item
                if name == "userName":
                    iam.name = item

        elif user['type'] == "IAMGroup":
            iam: Group = Group()

        for name, item in user.items():
            if name == "principalId": iam.principalId = item
            if name == "arn": iam.arn = item
            if name == "accountId": iam.accountID = item

        return iam
