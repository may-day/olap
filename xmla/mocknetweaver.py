from httmock import urlmatch, HTTMock, response, urlparse, first_of
import sys

class HTTMockBytes(HTTMock):
    def intercept(self, request):
        url = urlparse.urlsplit(request.url)
        res = first_of(self.handlers, url, request)
        if isinstance(res, bytes):
            return response(content=res)
        else:
            return super(HTTMockBytes, self).intercept(request)
            
@urlmatch(scheme="http", netloc='my-funky-sap-bw', path="/fake/xmla", method="POST")
def dummy(url, request):
    with open(sys.argv[1], 'rb') as f:
        content = f.read()
    return content

import olap.xmla.xmla as xmla

p=xmla.XMLAProvider()
c=p.connect("file:///home/norman/workspace/olap/xmla/sap.wsdl", location="http://my-funky-sap-bw/fake/xmla")
with HTTMockBytes(dummy):
    c.getDatasources()
