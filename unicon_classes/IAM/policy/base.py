from typing import List, Dict


class PolicyStatement:
    def __init__(self, statement: dict):
        self.sid = ""
        self.effect = ""
        self.actions: Dict[list] = {}
        self.resource = []
        self.condition = {}

    def _decode(self, statement: dict):
        for name, item in statement:
            if name == "Sid": self.sid = item
            if name == "Effect": self.effect = item
            if name == "Condition": self.condition = item
            if name == "Resource": self.resource = item
            if name == "Action": self.actions = self.__decode_action(item)

    @staticmethod
    def __decode_action(in_action) -> dict:
        ret: dict = {}
        if isinstance(in_action, list):
            for action in in_action:
                temp = action.split(":")
                if temp[0] in ret:
                    ret[temp[0]].append(temp[1])
        elif isinstance(in_action, str):
            temp = in_action.split(":")
            if temp[0] in ret:
                ret[temp[0]].append(temp[1])
        return ret


class BasePolicy:
    def __init__(self, policy=None):
        if policy is None:
            policy = {}
        self.version = ""
        self.statements: List[PolicyStatement] = []
        self._decode(policy)

    def _decode(self, policy: dict):
        for name, item in policy.items():
            if name == "Version": self.version = item
            if name == "Statement":
                for statement in item:
                    self.statements.append(PolicyStatement(statement=statement))
