from typing import List, Dict
import json

class PolicyStatement:
    def __init__(self, statement: dict):
        self.sid = ""
        self.effect = ""
        self.actions: Dict[list] = {}
        self.resource = []
        self.condition = {}
        self._decode(statement=statement)

    def _decode(self, statement: dict):
        for name, item in statement.items():
            if name == "Sid": self.sid = item
            if name == "Effect": self.effect = item
            if name == "Condition": self.condition = item
            if name == "Resource": self.resource = item
            if name == "Action": self.actions = self.__decode_action(item)

    def __str__(self):
        return (
"""Sid: {0}, 
Effect: {1}, 
Condition: {2}, 
Resource: {3},
Action: {4}
""".format(self.sid,self.effect, self.condition, self.resource, json.dumps(self.actions))
)

    @staticmethod
    def __decode_action(in_action) -> dict:
        ret: dict = {}
        if isinstance(in_action, list):
            for action in in_action:
                if ':' not in action:
                    ret[action] = [action]
                    continue
                temp = action.split(":")
                if temp[0] in ret:
                    ret[temp[0]].append(temp[1])
                else:
                    ret[temp[0]] = [temp[1]]
        elif isinstance(in_action, str):
            if ':' not in in_action:
                ret[in_action] = [in_action]
            else:
                temp = in_action.split(":")
                if temp[0] in ret:
                    ret[temp[0]].append(temp[1])
                else:
                    ret[temp[0]] = [temp[1]]
        return ret


class BasePolicy:
    def __init__(self, policy=None):
        if policy is None:
            policy = {}
        self.version = ""
        self.statements: List[PolicyStatement] = []
        self._decode(policy)

    def __str__(self):
        return """
        version: {0} 
        statements:
            {1}
        """.format(self.version, '\n'.join(map(str, self.statements)))

    def _decode(self, policy: dict):
        for name, item in policy.items():
            if name == "Version": self.version = item
            if name == "Statement":
                for statement in item:
                    self.statements.append(PolicyStatement(statement=statement))
