from unicon_classes.IAM.policy.base import BasePolicy


class GroupPolicy(BasePolicy):
    def __init__(self, policy=None):
        super().__init__(policy)
        if policy is None:
            policy = {}
        pass
