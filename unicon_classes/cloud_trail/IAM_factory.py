from unicon_classes.IAM import IAMUser, IAMBasic

class IAMFactory:

    def create(self, user: dict):
        iam = IAMBasic()
        if user['type'] == "IAMUser":
            iam = IAMUser()

        for name, item in user.items():
            