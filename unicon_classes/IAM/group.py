import unicon_classes.IAM.base as IAMBase
import unicon_classes.IAM.user as IAMUser
from datetime import datetime
from boto3_type_annotations.iam import Client
from typing import List
import boto3


class Group (IAMBase.Base):
    def __init__(self, name= None):
        super().__init__()
        self.type = "IAMGroup"
        self.path = ""
        self.groupID = ""
        self.createDate: datetime = None
        self.users: List[IAMUser.User] = None
        if name is not None:
            self.name = name
            self.re_sync()

    def __re_sync_update_group(self, group: dict):
        for name, item in group.items():
            if name == "Path": self.path = item
            if name == "GroupName": self.name = item
            if name == "GroupId": self.groupID = item
            if name == "Arn": self.arn = item
            if name == "CreateDate": self.createDate = item

    @staticmethod
    def create(group_name):
        client: Client = boto3.client('iam')
        response = client.create_group(GroupName=group_name)
        newgroup = Group()
        newgroup.__re_sync_update_group(response['Group'])
        return newgroup

    def delete(self):
        self.re_sync()
        client: Client = boto3.client('iam')
        for user in self.users:
            client.remove_user_from_group(GroupName=self.name, UserName=user.name)
        client.delete_group(GroupName=self.name)

    def add_to_group(self,  user: IAMUser.User):
        client: Client = boto3.client('iam')
        client.add_user_to_group(GroupName=self.name, UserName=user.name)
        self.re_sync()

    def in_group(self, user: IAMUser.User)->bool:
        if self.users is None:
            return False
        for test_user in self.users:
            if test_user == user:
                return True
        return False

    def re_sync(self):
        if self.name != "":
            client: Client = boto3.client('iam')
            response: dict = client.get_group(GroupName=self.name)
            if "Group" in response and "Users" in response:
                self.__re_sync_update_group(response['Group'])
                self.users = []
                for user in response["Users"]:
                    new_user = IAMUser.User()
                    new_user.update_user(user)
                    self.users.append(new_user)


