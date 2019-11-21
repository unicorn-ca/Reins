from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode
from typing import List


class CodeCommitRequestParameter:
    def __init__(self, params: dict):
        self.branch = ""
        self.commit = ""
        self.branch_path = ""
        self.__decode(params= params)

    def __decode(self, params:dict):
        for name, item in params.items():
            name = name.lower()
            if name == 'commit': self.commit = item
            if name == 'ref' :
                self.branch_path = item
                temp = self.branch_path.split("/")
                self.branch = temp[-1]


class CodeCommit(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.data_transferred = False
        self.protocol = ""
        self.capabilities:list = []
        self.branches: List[CodeCommitRequestParameter] = []
        self.repo_name = ""
        self.repo_id = ""
        self.__code_commit_decode(self.cloud_trail_event)

    def __code_commit_decode(self, event:dict):
        if self.request_parameters:
            for name, item in self.request_parameters.items():
                if name == "references":
                    for param in item:
                        self.branches.append(CodeCommitRequestParameter(param))
        for name, item in event.items():
            if name == 'additionalEventData':
                for name_inner , item_inner  in item.items():
                    if name_inner == "protocol" : self.protocol = item_inner
                    if name_inner == "dataTransferred": self.data_transferred = item_inner
                    if name_inner == "repositoryName": self.repo_name = item_inner
                    if name_inner == "repositoryId": self.repo_id = item_inner
                    if name_inner == "capabilities": self.capabilities = item_inner





