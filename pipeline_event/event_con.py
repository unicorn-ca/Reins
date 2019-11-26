from typing import List
import json

from pipeline_event.event import Event as EventInst
from pipeline_event.artifacts import Artifacts
from pipeline_event.artifacts_con import Artifacts as ArtifactsCon


class Event(EventInst):

    def __init__(self, event):
        self.id: str = ""
        self.account_id: str = ""
        self.input_artifacts: List[Artifacts] = []
        self.output_artifacts: List[Artifacts] = []
        self.lambda_name: str = ""
        self.params = {}
        self.continuation_token = ""
        self.raw_params = {}
        self.__convert(event)

    def set_account_id(self, item):
        self.account_id = item

    def set_id(self, item):
        self.id = item

    def set_params(self, item: dict):
        self.params = item

    def set_raw_params(self, item):
        self.raw_params = item

    def set_continuation_token(self, item):
        self.continuation_token = item

    def set_input_artifacts(self, item:List[Artifacts]):
        self.input_artifacts = item

    def set_output_artifacts(self, item:List[Artifacts]):
        self.output_artifacts = item

    def set_lambda_name(self, item):
        self.lambda_name = item

    def get_account_id(self):
        return self.account_id

    def get_id(self):
        return self.id

    def get_params(self):
        return self.params

    def get_raw_params(self) -> dict:
        return self.raw_params

    def get_continuation_token(self):
        return self.continuation_token

    def get_input_artifacts(self) -> List[Artifacts]:
        return self.input_artifacts

    def get_output_artifacts(self) -> List[Artifacts]:
        return self.output_artifacts

    def get_lambda_name(self):
        return self.lambda_name

    def __add_artifact(self,artifact: dict, data: dict) -> Artifacts:
        cred = {}
        encrypt = {}
        if "artifactCredentials" in data:
            cred = data["artifactCredentials"]
        if "encryptionKey" in data:
            encrypt = data["encryptionKey"]
        return ArtifactsCon(artifact,cred,encrypt)

    def __convert(self,event: dict):
        if "CodePipeline.job" in event:
            event = event["CodePipeline.job"]
            for name, item in event.items():
                if name == "id":
                    self.set_id(item)
                if name == "accountId":
                    self.set_account_id(item)
                if name == "data":
                    for data_name, data_item in item.items():
                        if data_name == "actionConfiguration":
                            if "configuration" in data_item:
                                self.set_raw_params(data_item["configuration"])
                                if "UserParameters" in data_item["configuration"]:
                                    if isinstance(data_item["configuration"]["UserParameters"], str):
                                        self.set_params(json.loads(data_item["configuration"]["UserParameters"]))
                                    else:
                                        self.set_params(data_item["configuration"]["UserParameters"])
                                if "FunctionName" in data_item["configuration"]:
                                    self.set_lambda_name(data_item["configuration"]["FunctionName"])
                        if data_name == "inputArtifacts":
                            temp = []
                            for artifact in data_item:
                                temp.append(self.__add_artifact(artifact, item))
                            self.set_input_artifacts(temp)
                        if data_name == "outputArtifacts":
                            temp = []
                            for artifact in data_item:
                                temp.append(self.__add_artifact(artifact, item))
                            self.set_output_artifacts(temp)

                        if data_name == "continuationToken":
                            self.set_continuation_token(data_item)

