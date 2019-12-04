from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode


class IAM(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.__iam_decode(self.cloud_trail_event)

    def __iam_decode(self, event: dict):
        pass





