from unicon_classes.cloud_trail import Event
from unicon_classes.IAM.IAM_factory import IAMFactory
from unicon_classes.IAM.base import Base as IAMBasic


class BasicDecode(Event):
    def __init__(self, event: dict):
        super().__init__(event=event, json_decode_cloud_trail_event=True)
        self.identity: IAMBasic = None
        self.aws_region = ""
        self.source_IP_address = ""
        self.user_agent = ""
        self.request_parameters = {}
        self.recipient_account_id = ""
        self.error = False
        self.error_code = ""
        self.error_message = ""
        self.__extract(self.cloud_trail_event)

    def __extract(self, log: dict):
        for name, item in log.items():
            name = name.lower()
            if name == 'awsregion': self.aws_region = item
            if name == 'sourceipaddress': self.source_IP_address = item
            if name == 'useragent': self.user_agent = item
            if name == 'requestparameters': self.request_parameters = item
            if name == 'recipientaccountid': self.aws_region = item
            if name == 'eventtype': self.event_type = item
            if name == 'useridentity' : self.identity = IAMFactory.create(item)
            if name == 'errorCode':
                self.error_code = item
                self.error = True
            if name == 'errorMessage':
                self.error_message = item
                self.error = True


