import requests.sessions
from . import adapters
import logging

log = logging.getLogger(__name__)

class Session(requests.sessions.Session):
    def get_adapter(self, url):
        adapter=super(Session, self).get_adapter(url)
        return self.wrap_adapter(adapter)

    def wrap_adapter(self, adapter):
        return adapters.FixedConnectionAdapter(adapter)

    def send(self, request, **kwargs):
        try:
            return super(Session, self).send(request, **kwargs)
        except Exception as e:
            # find possible hook to call in case of exception
            for h in request.hooks["response"]:
                if hasattr(h, "call_on_exception"):
                    h(request)
            raise
