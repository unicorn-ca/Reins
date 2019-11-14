from unicon_classes.cloud_trail import Event

class BasicDecode(Event):
    def __init__(self, event:dict):
        super().__init__(event=event, json_decode_cloud_trail_event=True)
        self.aws_region = ""
        self.source_IP_address = ""
        self.user_agent = ""
        self.request_parameters = {}
        self.recipient_account_id = ""

    def __extract(self, log: dict):
        for name, item in log.items():
            if name == 'awsRegion': self.aws_region = item
            if name == 'sourceIPAddress': self.source_IP_address = item
            if name == 'userAgent': self.user_agent = item
            if name == 'requestParameters': self.request_parameters = item
            if name == 'recipientAccountId': self.aws_region = item


