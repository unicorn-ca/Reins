from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode


class STS(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.__sts_decode(self.cloud_trail_event)

    def __sts_decode(self, event: dict):
        pass





