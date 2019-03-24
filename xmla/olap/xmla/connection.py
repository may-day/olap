'''
Created on 18.04.2012

@author: norman
'''
from .interfaces import XMLAException
from zeep import Client
from zeep.exceptions import Fault
from zeep.transports import Transport
import types
from .formatreader import TupleFormatReader
from .utils import *
import logging
from requests_kerberos import HTTPKerberosAuth

logger = logging.getLogger(__name__)

from zeep import Plugin
from zeep import xsd
from lxml import etree
from xml.etree import ElementTree as ET

ns = {"soap-env":"http://schemas.xmlsoap.org/soap/envelope/"}
# the following along with changes to the wsdl (elementFormDefault="unqualified") is needed
# to make it fly with icCube, which expects elements w/o namespace prefix
class LogRequest(Plugin):
    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True).decode("utf-8"))

    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True).decode("utf-8"))

class UseDefaultNamespace(Plugin):
    def xegress(self, envelope, http_headers, operation, binding_options):
        body = envelope.find('soap-env:Body', ns)
        for d in body:
            if '}' in d.tag:
                print(type(d.tag))
                d.tag = d.tag.split('}', 1)[1]  # strip all namespaces
                d.nsmap[None]="urn:schemas-microsoft-com:xml-analysis"

class SessionPlugin(Plugin):
  def __init__(self, xmlaconn):
      self.xmlaconn = xmlaconn

  def ingress(self, envelope, http_headers, operation):
      if self.xmlaconn.getListenOnSessionId():
          self.xmlaconn.setSessionId(envelope.xpath("/Envelope/Header/Session").attrib.get("SessionId"))

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)

# lsit of XMLA1.1 rowsets: 
xmla1_1_rowsets = ["DISCOVER_DATASOURCES",
                   "DISCOVER_PROPERTIES", 
                   "DISCOVER_SCHEMA_ROWSETS",
                   "DISCOVER_ENUMERATORS",
                   "DISCOVER_LITERALS",
                   "DISCOVER_KEYWORDS",
                   "DBSCHEMA_CATALOGS",
                   "DBSCHEMA_COLUMNS",
                   "DBSCHEMA_TABLES",
                   "DBSCHEMA_TABLES_INFO",
                   "DBSCHEMA_PROVIDER_TYPES",
                   "MDSCHEMA_ACTIONS",
                   "MDSCHEMA_CUBES",
                   "MDSCHEMA_DIMENSIONS",
                   "MDSCHEMA_FUNCTIONS",
                   "MDSCHEMA_HIERARCHIES",
                   "MDSCHEMA_MEASURES",
                   "MDSCHEMA_MEMBERS",
                   "MDSCHEMA_PROPERTIES",
                   "MDSCHEMA_SETS"
                   ]

class XMLAConnection(object):
    
    @classmethod
    def addMethod(cls, funcname, func):
#        return setattr(cls, funcname, types.MethodType(func, None, cls))
        return setattr(cls, funcname, func)

        
    @classmethod
    def setupMembers(cls):
        def getFunc(schemaName):
            return lambda this, *args, **kw: cls.Discover(this, 
                                                          schemaName, 
                                                          *args, **kw)
        
        for schemaName in xmla1_1_rowsets:
            mname = schemaNameToMethodName(schemaName)
            cls.addMethod( mname, getFunc(schemaName) )

    def __init__(self, url, location, username, password, spn, sslverify, **kwargs):

        transport = Transport()
        kw = {}
        if spn:
            service, host = spn.split("@",1)
            kw["service"]=service
            kw["hostname_override"]=host
        if username:
            kw["principal"] = username
        if "auth" in kwargs:
            transport.session.auth = kwargs["auth"]
            del kwargs["auth"]
        else:
            transport.session.auth = HTTPKerberosAuth(**kw)

        self.sessionplugin=SessionPlugin(self)
        self.client = Client(url, 
                             transport=transport, 
                             # cache=None, unwrap=False,
                             plugins=[UseDefaultNamespace(), self.sessionplugin, LogRequest()])
        self.service = self.client.create_service('{urn:schemas-microsoft-com:xml-analysis}MsXmlAnalysisSoap', location)
        self.client.set_ns_prefix(None, "urn:schemas-microsoft-com:xml-analysis")
        # optional, call might fail
        self.getMDSchemaLevels = lambda *args, **kw: self.Discover("MDSCHEMA_LEVELS", 
                                                                   *args, **kw)
        self.setListenOnSessionId(False)
        self.setSessionId(None)
             

    def getListenOnSessionId(self):
        return self.listenOnSessionId

    def setListenOnSessionId(self, trueOrFalse):
        self.listenOnSessionId = trueOrFalse

    def setSessionId(self, sessionId):
        self.sessionId = sessionId
        
    def Discover(self, what, restrictions=None, properties=None):
        rl = None
        pl = None
        if restrictions:
            rl = {"RestrictionList":restrictions}
        if properties:
            pl = {"PropertyList":properties}
            
        try:
            import pdb; pdb.set_trace()
            doc=self.service.Discover(what, rl, pl)
            res = getattr(doc.DiscoverResponse["return"].root, "row", [])
            if res:
                res = aslist(res)
        except Fault as fault:
            raise XMLAException(fault.message, dictify(fault))
        logger.debug( res )
        return res


    def Execute(self, command, dimformat="Multidimensional", 
                axisFormat="TupleFormat", **kwargs):
        nsmap={None:"urn:schemas-microsoft-com:xml-analysis"}
        if isinstance(command, stringtypes):
            cmd = etree.Element("{urn:schemas-microsoft-com:xml-analysis}Statement", nsmap=nsmap)
            cmd.text = command
            command = cmd
        props = {"Format":dimformat, "AxisFormat":axisFormat}
        props.update(kwargs)
        plist = etree.Element("PropertyList", nsmap=nsmap)
        for (k,v) in props.items():
            e=etree.SubElement(plist, k)
            e.text=v
        try:
            
            res = self.service.Execute(Command=command, Properties=plist)
            root = res.body["return"]["_value_1"]
            return TupleFormatReader(fromETree(root))
        except Fault as fault:
            raise XMLAException(fault.message, dictify(fault))
        
        
    def BeginSession(self):
        bs= self.client.factory.create("BeginSession")
        bs._mustUnderstand = 1
        sess= self.client.factory.create("Session")
        sess._mustUnderstand = 1
        self.client.set_options(soapheaders={"BeginSession":bs})
        self.setListenOnSessionId(True)
        self.client.service.Execute({"Statement":None})
        self.setListenOnSessionId(False)
        #print(self.client)
        sess._SessionId=self.sessionId
        self.client.set_options(soapheaders=sess)
        
    def EndSession(self):
        if self.sessionId is not None:
            es= self.client.factory.create("EndSession")
            es._mustUnderstand = 1
            es._SessionId = self.sessionId
            self.client.set_options(soapheaders={"EndSession":es})
            self.service.Execute({"Statement":None})
            self.setSessionId(None)
            self.client.set_options(soapheaders=None)

                
XMLAConnection.setupMembers()
