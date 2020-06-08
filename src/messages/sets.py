from spade.template import Template
from spade.message import Message

SETS_TOPIC = "sets"

class SetsTemplate(Template):
    def __init__(self):
        super(Template, self).__init__()
        self.set_metadata("conversation-id", SETS_TOPIC)

class SetsMessage(Message):
    def __init__(self, to=None, body=None):
        super(Message, self).__init__()
        if isinstance(to, str):
            self.to = to
        else:
            self.to = str(to)

        self.set_metadata("conversation-id", SETS_TOPIC)
        self.body = str(body)

    def template(to=None):
        template = SetsTemplate()
        template.to = to
        return template
