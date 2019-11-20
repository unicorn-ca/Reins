from unicon_classes.cloud_trail import Event, CodeCommitEvent


class EventFactory:

    def create(event:dict)-> Event:
        if 'EventSource' in event:
            if event['EventSource'] == "codecommit.amazonaws.com":
                return CodeCommitEvent(event)
            else:
                return Event(event)
        raise Exception("The Event Input doesn't have a EventSource")
