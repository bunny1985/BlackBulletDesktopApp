


class AbstractEventHandler(EventType):
    def __init__(self):
        self.type = EventType

    def canHandle(self):
        return self.type
    @abc.abstractclassmethod
    def handle(event ):
        """Method that should handle event."""
        pass




    
