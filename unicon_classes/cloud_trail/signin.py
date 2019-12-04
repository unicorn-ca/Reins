from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode


class SignIn(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.__sign_in_decode(self.cloud_trail_event)

    def __sign_in_decode(self, event: dict):
        pass





