import requests
import requests_mock
from zeep import Plugin
import olap.xmla.utils as utils

def make_comparable(s):
    if s.startswith("<?xml"):
        s = s.split("?>",1)[1]
    s = "".join(s.split()).lower()
    return s

def conversation_matcher(m, testname):
    def match(req):
        conversation = getattr(m, "conversation", {})
        it = iter(conversation.get(testname, []))
        lu = make_comparable(req.text)
        for kind, envel in it:
            if kind == "request":
                cand = make_comparable(envel)
                if lu == cand:
                    # reply with next response we find
                    for kind, envel in it:
                        if kind == "response":
                            return requests_mock.create_response(req, text=envel)

        return None

    return match

class LogRequest(Plugin):
    def __init__(self, enabled):
        self.enabled = enabled
        self.hist = {}
        self.prefix = ""
        
    def egress(self, envelope, http_headers, operation, binding_options):
        str_envelope=utils.etree_tostring(envelope)
        self.hist.setdefault(self.prefix,  []).append(("request", str_envelope))
        if self.enabled:
            print(str_envelope)

    def ingress(self, envelope, http_headers, operation):
        str_envelope=utils.etree_tostring(envelope)
        self.hist.setdefault(self.prefix,  []).append(("response", str_envelope))
        if self.enabled:
            print(str_envelope)

    def enable(self):
        self.enabled=True

    def disable(self):
        self.enabled=False

    def saveConversation(self, fname):
        with open(fname, "w+") as f:
            f.write('conversation={\n')
            for k in sorted(self.hist.keys()):
                f.write('    "{}":[\n'.format(k))
                for req_res in self.hist[k]:
                    f.write('        ("{}", """{}"""),\n'.format(*req_res))
                f.write('    ],\n')
            f.write('}')

def mockedsession(conversation, testname):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    adapter.add_matcher(conversation_matcher(conversation, testname))
    session.mount('mock', adapter)
    return session
