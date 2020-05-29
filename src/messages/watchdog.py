from spade.template import Template
from spade.message import Message

WATCHDOG_TOPIC = "watchdog"

class WatchdogTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", WATCHDOG_TOPIC)
        self.set_metadata("performative", "inform")

class WatchdogMessage(Message):
    def __init__(self, sender, receiver, body=None):
        super(Message, self).__init__()
        self.sender = sender
        self.to = receiver
        self.set_metadata("conversation-id", WATCHDOG_TOPIC)
        self.set_metadata("performative", "inform")
        self.body = body
