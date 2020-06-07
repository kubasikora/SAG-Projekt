from spade.template import Template
from spade.message import Message

RISK_TOPIC = "risk"

class RiskTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", RISK_TOPIC)

class RiskMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", RISK_TOPIC)
        self.body = str(body)

    def template(to=None):
        template = RiskTemplate()
        template.to = to
        return template
