from abc import ABC, abstractmethod
from typing import List
from pipeline_event.artifacts import Artifacts


class Event(ABC):
    @abstractmethod
    def get_account_id(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_params(self) -> dict:
        pass

    @abstractmethod
    def get_raw_params(self) -> dict:
        pass

    @abstractmethod
    def get_continuation_token(self):
        pass

    @abstractmethod
    def get_input_artifacts(self) -> List[Artifacts]:
        pass

    @abstractmethod
    def get_output_artifacts(self) -> List[Artifacts]:
        pass

    @abstractmethod
    def get_lambda_name(self):
        pass

    @abstractmethod
    def set_account_id(self, item):
        pass

    @abstractmethod
    def set_id(self, item):
        pass

    @abstractmethod
    def set_params(self, item):
        pass

    @abstractmethod
    def set_raw_params(self, item):
        pass

    @abstractmethod
    def set_continuation_token(self, item):
        pass

    @abstractmethod
    def set_input_artifacts(self, item: List[Artifacts]):
        pass

    @abstractmethod
    def set_output_artifacts(self, item: List[Artifacts]):
        pass

    @abstractmethod
    def set_lambda_name(self, item):
        pass

    def __str__(self):
        return """AccountID = {0}
        ID = {1}
        Params = {2}
        Lambda Name = {3}""".format(self.get_account_id(), self.get_id(), self.get_params(), self.get_lambda_name())
