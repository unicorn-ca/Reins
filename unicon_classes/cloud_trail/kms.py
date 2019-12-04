from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode


class KMS(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.__kms_decode(self.cloud_trail_event)

    def __kms_decode(self, event: dict):
        pass





