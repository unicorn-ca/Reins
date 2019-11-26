import unicon_classes.IAM.base as IAMBasic
from datetime import datetime
from boto3_type_annotations.iam import Client
from typing import List
from unicon_classes.IAM.policy.user import UserPolicies
import boto3
import json


class User(IAMBasic.Base):
    def __init__(self, name= None):
        super().__init__()
        self.type = "IAMUser"
        self.accessKeyId = ""
        self.createDate: datetime = None
        self.passwordLastUsed: datetime = None
        self.path = ""
        self.userID = ""
        self.tags: List[dict] = None
        self.permissionsBoundaryType = ""
        self.permissionsBoundaryArn = ""
        self.__policy_cache = None

        if name is not None:
            self.name = name
            self.re_sync()

    def _get_policies(self) -> List[UserPolicies]:
        if self.__policy_cache is None:
            client: Client = boto3.client('iam')
            truncated = True
            marker = ""
            self.__policy_cache = []
            while truncated:
                truncated = False
                if marker == "":
                    policies = client.list_attached_user_policies(
                        UserName=self.name
                    )
                else:
                    policies = client.list_attached_user_policies(
                        UserName=self.name,
                        Marker=marker
                    )
                for name, item in policies.items():
                    if name == 'IsTruncated' : truncated = item
                    if name == 'Marker': marker = item
                    if name == 'AttachedPolicies' :
                        for policy in item:
                            temp = client.get_policy(PolicyArn=policy['PolicyArn'])
                            temp = client.get_policy_version(PolicyArn=policy['PolicyArn'], VersionId=temp['Policy']['DefaultVersionId'])
                            temp = temp['PolicyVersion']['Document']
                            self.__policy_cache.append(UserPolicies(temp))
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

    @staticmethod
    def get_all_users() -> list:
        client: Client = boto3.client('iam')
        more = True
        marker = ""
        ret = []
        while more:
            more = False
            if marker == "":
                luser = client.list_users()
            else:
                luser = client.list_users(Marker=marker)
            for name, item in luser.items():
                if name == 'Marker': marker = item
                if name == 'IsTruncated': more = item
                if name == 'Users':
                    for user_dict in item:
                        temp = User()
                        temp.update_user(user_dict)
                        ret.append(temp)
        return ret

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
        return group.in_group(self)
