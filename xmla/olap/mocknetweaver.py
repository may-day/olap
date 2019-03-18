from httmock import urlmatch, HTTMock

@urlmatch(scheme="http", netloc='localhost:8080', path="/mondrian/xmla", method="POST")
def dummy(url, request):
    with open("/home/norman/workspace/olap/xmla/tests/discover_datasources.xml", 'r') as f:
        content = f.read()
    return content

import olap.xmla.xmla as xmla

p=xmla.XMLAProvider()
c=p.connect(location="http://localhost:8080/mondrian/xmla")
with HTTMock(dummy):
    c.getDatasources()
