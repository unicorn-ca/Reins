from unicon_classes.cloud_trail.event_decode import BasicDecode as EventDecode


# lambda.amazonaws.com
class Lambda(EventDecode):
    def __init__(self, event: dict):
        super().__init__(event)
        self.__lambda_decode(self.request_parameters)

    def __lambda_decode(self, event:dict):
       pass






