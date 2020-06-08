from spade.template import Template
from spade.message import Message

INACTIVE_TOPIC = "inactive"

class InactiveTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", INACTIVE_TOPIC)
        self.set_metadata("performative", "inform")

class InactiveMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", INACTIVE_TOPIC)
        self.set_metadata("performative", "inform")
        
        self.body = str(body)

    def template(to=None):
        template = InactiveTemplate()
        template.to = to
        return template