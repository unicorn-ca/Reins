import unicon_classes.IAM.base as IAMBasic
from datetime import datetime
from boto3_type_annotations.iam import Client
from typing import List
from unicon_classes.IAM.policy.user import UserPolicies
import boto3


class Root(IAMBasic.Base):
    def __init__(self, name= None):
        super().__init__()
        self.type = "Root"
        self.accessKeyId = ""
        self.createDate: datetime = None
        self.passwordLastUsed: datetime = None
        self.path = ""
        self.userID = ""
        self.tags: List[dict] = None
        self.permissionsBoundaryType = ""
        self.permissionsBoundaryArn = ""
        self.__policy_cache = None
        self.name = "root"

    def _get_policies(self) -> List[UserPolicies]:
        if self.__policy_cache is None:
            self.__policy_cache = [UserPolicies({"Statement":{
                [{"Action" : "*:*"}]
            }})]
        return self.__policy_cache

    def update_user(self, user: dict):
        for name, item in user.items():
            if name == "Path": self.path = item
            if name == "UserName": self.name = item
            if name == "UserId": self.userID = item
            if name == "Arn": self.arn = item
            if name == "CreateDate": self.createDate = item
            if name == "PasswordLastUsed": self.passwordLastUsed = item
            if name == "PermissionsBoundary":
                for in_name, in_item in item.items():
                    if in_name == 'PermissionsBoundaryType': self.permissionsBoundaryType = in_item
                    if in_name == 'PermissionsBoundaryArn' : self.permissionsBoundaryArn = in_item
            if name == "Tags": self.tags = item

    def __eq__(self, other):
        if isinstance(other, User):
            if other.arn == self.arn and (other.name == self.name or other.userID == self.userID):
                return True
        return False


    def re_sync(self):
        if self.name != "":
            client: Client = boto3.client('iam')
            response:dict = client.get_user(UserName=self.name)
            if 'User' in response:
                self.update_user(response['User'])
            else:
                raise Exception("Sync Response Didn't have User Key")
        else:
            raise Exception("Name Isn't Set When Trying Sync")

    def in_group(self, group) -> bool:
        return True
