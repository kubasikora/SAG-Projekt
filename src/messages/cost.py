from spade.template import Template
from spade.message import Message

COST_TOPIC = "cost"

class CostTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", COST_TOPIC)
        self.set_metadata("performative", "request")
        self.set_metadata("save", "True")
        
class CostMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", COST_TOPIC)
        self.set_metadata("performative", "request")
        self.set_metadata("save", "True")
        
        self.body = str(body)

    def template(to=None):
        template = CostTemplate()
        template.to = to
        return template
