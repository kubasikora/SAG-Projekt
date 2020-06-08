from spade.template import Template
from spade.message import Message

STATES_TOPIC = "states"

class StatesTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", STATES_TOPIC)

class StatesMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", STATES_TOPIC)
        self.set_metadata("performative", "inform")
        self.body = str(body)

    def template(to=None):
        template = StatesTemplate()
        template.to = to
        return template
