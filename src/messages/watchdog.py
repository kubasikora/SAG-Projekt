from spade.template import Template
from spade.message import Message

WATCHDOG_TOPIC = "watchdog"

class WatchdogTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", WATCHDOG_TOPIC)
        self.set_metadata("performative", "inform")

class WatchdogMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", WATCHDOG_TOPIC)
        self.set_metadata("performative", "inform")
        
        self.body = str(body)

    def template(to=None):
        template = WatchdogTemplate()
        template.to = to
        return template