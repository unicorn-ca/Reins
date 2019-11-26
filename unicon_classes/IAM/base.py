from typing import List
from unicon_classes.IAM.policy.base import BasePolicy


class Base():
    def __init__(self, name= ""):
        self.type = ""
        self.name = name
        self.accountID = ""
        self.arn = ""
        self.principalId = ""
        self._policies: List[BasePolicy] = None

    @property
    def policies(self):
        if self._policies is None:
            self._policies = self._get_policies()
        return self._policies

    @policies.setter
    def policies(self, value: BasePolicy):
        self._policies = value

    def _get_policies(self) -> List[BasePolicy]:
        pass


