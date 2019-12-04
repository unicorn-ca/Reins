from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode
from typing import List

class CodePipelineActions:
    def __init__(self, event: dict):
        self.name = ""
        self.owner = ""
        self.version = ""
        self.category = ""
        self.provider = ""
        self.input_artifacts: List[str] = []
        self.output_artifacts: List[str] = []
        self.run_order = 0
        self.s3_bucket = ""
        self.s3_object_key = ""

    def __decode(self, event: dict):
        for name, item in event:
            if name == "name": self.name = item
            if name == "actionType":
                for type_name, type_item in item.items():
                    if type_name == "owner": self.owner = type_item
                    if type_name == "version": self.version = type_item
                    if type_name == "category": self.category = type_item
                    if type_name == "provider": self.provider = type_item
            if name == "inputArtifacts": self.input_artifacts = map(lambda x: x['name'], item)
            if name == "outputArtifacts": self.output_artifacts = map(lambda x: x['name'], item)
            if name == "runOrder" : self.run_order = item
            if name == "configuration":
                for conf_name, conf_item in item.items():
                    if conf_name == "S3Bucket": self.s3_bucket = conf_item
                    if conf_name == "S3ObjectKey": self.s3_object_key = conf_item

class CodePipelineStages:
    def __init__(self, event: dict):
        self.actions: List[CodePipelineActions] = []
        self.name = ""
        self.__decode(event)

    def __decode(self,event:dict):
        for name, item in event.items():
            if name == "actions":
                for action in item:
                    self.actions.append(CodePipelineActions(action))
            if name == "name": self.name = item

# codepipeline.amazonaws.com
class CodePipeline(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.old_role_arn = ""
        self.old_pipeline_name = ""
        self.old_version = 0
        self.new_role_arn = ""
        self.new_pipeline_name = ""
        self.new_version = 0
        self.old_stages: List[CodePipelineStages] = []
        self.new_stages: List[CodePipelineStages] = []
        self.__code_commit_decode(self.cloud_trail_event)

    def __code_commit_decode(self, event:dict):
        for name, item in event.items():
            if name == 'requestParameters':
                if 'pipeline' in item:
                    for name_inner, item_inner in item['pipeline'].items():
                        if name_inner == 'name': self.old_pipeline_name = item_inner
                        if name_inner == 'roleArn': self.old_role_arn = item_inner
                        if name_inner == "version": self.old_version = item_inner
                        if name_inner == 'stages':
                            self.old_stages.append(CodePipelineStages(item['pipeline']))
            if name == 'responseElements':
                if 'pipeline' in item:
                    for name_inner, item_inner in item['pipeline'].items():
                        if name_inner == 'name': self.new_pipeline_name = item_inner
                        if name_inner == 'roleArn': self.new_role_arn = item_inner
                        if name_inner == "version": self.new_version = item_inner
                        if name_inner == 'stages':
                            self.new_stages.append(CodePipelineStages(item['pipeline']))






