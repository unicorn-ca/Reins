from abc import ABC, abstractmethod
from unicon_classes.IAM.policy.base import BasePolicy


class Base(ABC):
    def __init__(self, name= ""):
        self.type = ""
        self.name = name
        self.accountID = ""
        self.arn = ""
        self.principalId = ""
        self._policy: BasePolicy = None

    @property
    def policy(self):
        if self._policy is None:
            self._policy = self._get_policy()
        return self._policy

    @policy.setter
    def policy(self, value:BasePolicy):
        self._policy = value

    @abstractmethod
    def _get_policy(self) -> BasePolicy:
        pass


