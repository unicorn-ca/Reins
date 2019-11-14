from unicon_classes.IAM.base import Base
from unicon_classes.IAM import IAMGroup
from datetime import datetime
from boto3_type_annotations.iam import Client
from typing import List
import boto3


class User (Base):
    def __init__(self):
        super().__init__()
        self.type = "IAMUser"
        self.accessKeyId = ""
        self.createDate: datetime = None
        self.passwordLastUsed: datetime = None
        self.path = ""
        self.userID = ""
        self.tags: List[dict] = None
        self.permissionsBoundary: dict = None

    def update_user(self, user: dict):
        for name, item in user.items():
            if name == "Path": self.path = item
            if name == "UserName": self.name = item
            if name == "UserId": self.userID = item
            if name == "Arn": self.arn = item
            if name == "CreateDate": self.createDate = item
            if name == "PasswordLastUsed": self.passwordLastUsed = item
            if name == "PermissionsBoundary": self.permissionsBoundary = item
            if name == "Tags": self.tags = item

    def __eq__(self, other):
        if isinstance(other,User):
            if other.arn == self.arn and (other.name == self.name or other.userID == self.userID):
                return True
        return False

    def re_sync(self):
        if self.name != "":
            client: Client = boto3.client('iam')
            response:dict = client.get_user(self.name)
            if 'User' in response:
                self.update_user(response['User'])
            else:
                raise Exception("Sync Response Didn't have User Key")
        else:
            raise Exception("Name Isn't Set When Trying Sync")

    def in_group(self, group: IAMGroup) -> bool:
        return group.in_group(self)
