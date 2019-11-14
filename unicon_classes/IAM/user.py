from unicon_classes.IAM.base import Base


class User (Base):
    def __init__(self):
        super().__init__()
        self.type = "IAMUser"
