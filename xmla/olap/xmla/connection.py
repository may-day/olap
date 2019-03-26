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

logger = logging.getLogger(__name__)

from zeep import Plugin
from zeep import xsd
from lxml import etree
from xml.etree import ElementTree as ET

ns = {"soap-env":"http://schemas.xmlsoap.org/soap/envelope/"}
# the following along with changes to the wsdl (elementFormDefault="unqualified") is needed
# to make it fly with icCube, which expects elements w/o namespace prefix
class LogRequest(Plugin):
    def __init__(self, enabled=True):
        self.enabled = enabled

    def egress(self, envelope, http_headers, operation, binding_options):
        if self.enabled:
            print(etree.tostring(envelope, pretty_print=True).decode("utf-8"))

    def ingress(self, envelope, http_headers, operation):
        if self.enabled:
            print(etree.tostring(envelope, pretty_print=True).decode("utf-8"))

    def enable(self):
        self.enabled=True
    def disable(self):
        self.enabled=False

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
    #print(etree.tostring(envelope, pretty_print=True).decode("utf-8"))
    if self.xmlaconn.getListenOnSessionId():
        nsmap={'se': 'http://schemas.xmlsoap.org/soap/envelope/',
               'xmla': 'urn:schemas-microsoft-com:xml-analysis'}
        s=envelope.xpath("/se:Envelope/se:Header/xmla:Session", namespaces=nsmap)[0]
        sid=s.attrib.get("SessionId")
        self.xmlaconn.setSessionId(sid)

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

    def __init__(self, url, location, sslverify, **kwargs):

        transport = Transport()
        if "auth" in kwargs:
            transport.session.auth = kwargs["auth"]
            del kwargs["auth"]

        transport.session.verify = sslverify
        self.sessionplugin=SessionPlugin(self)
        plugins=[UseDefaultNamespace(), self.sessionplugin]

        if "log" in kwargs:
            log = kwargs.get("log")
            if isinstance(log, Plugin):
                plugins.append(log)
            elif log == True:
                plugins.append(LogRequest())
            del kwargs["log"]
            
        self.client = Client(url, 
                             transport=transport, 
                             # cache=None, unwrap=False,
                             plugins=plugins)

        self.service = self.client.create_service('{urn:schemas-microsoft-com:xml-analysis}MsXmlAnalysisSoap', location)
        self.client.set_ns_prefix(None, "urn:schemas-microsoft-com:xml-analysis")
        # optional, call might fail
        self.getMDSchemaLevels = lambda *args, **kw: self.Discover("MDSCHEMA_LEVELS", 
                                                                   *args, **kw)
        self.setListenOnSessionId(False)
        self.setSessionId(None)
        self._soapheaders=None
             

    def getListenOnSessionId(self):
        return self.listenOnSessionId

    def setListenOnSessionId(self, trueOrFalse):
        self.listenOnSessionId = trueOrFalse

    def setSessionId(self, sessionId):
        self.sessionId = sessionId
        
    def Discover(self, what, restrictions=None, properties=None):
        rl = None
        pl = None
        nsmap={None:"urn:schemas-microsoft-com:xml-analysis"}
        if restrictions:
            rl = etree.Element("RestrictionList", nsmap=nsmap)
            for (k,v) in restrictions.items():
                e=etree.SubElement(rl, k)
                if v is not None:
                    e.text=str(v)
        if properties:
            pl = etree.Element("PropertyList", nsmap=nsmap)
            for (k,v) in properties.items():
                e=etree.SubElement(pl, k)
                if v is not None:
                    e.text=str(v)
            
        try:
            #import pdb; pdb.set_trace()
            doc=self.service.Discover(RequestType=what, Restrictions=rl, Properties=pl, _soapheaders=self._soapheaders)
            root = fromETree(doc.body["return"]["_value_1"], ns="urn:schemas-microsoft-com:xml-analysis:rowset")
            res = getattr(root, "row", [])
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
            if command is not None:
                cmd.text = command
            command = cmd
        props = {"Format":dimformat, "AxisFormat":axisFormat}
        props.update(kwargs)
        plist = etree.Element("PropertyList", nsmap=nsmap)
        for (k,v) in props.items():
            e=etree.SubElement(plist, k)
            if v is not None:
                e.text=str(v)
        try:
            
            res = self.service.Execute(Command=command, Properties=plist, _soapheaders=self._soapheaders)
            root = res.body["return"]["_value_1"]
            return TupleFormatReader(fromETree(root))
        except Fault as fault:
            raise XMLAException(fault.message, dictify(fault))
        
        
    def BeginSession(self):
        bs= self.client.get_element("{urn:schemas-microsoft-com:xml-analysis}BeginSession")(mustUnderstand=1)
        self.setListenOnSessionId(True)
        #self.service.Execute("woop", _soapheaders={"BeginSession":bs})
        nsmap={None:"urn:schemas-microsoft-com:xml-analysis"}
        cmd = etree.Element("{urn:schemas-microsoft-com:xml-analysis}Statement", nsmap=nsmap)

        self.service.Execute(Command=cmd,_soapheaders={"BeginSession":bs})
        self.setListenOnSessionId(False)
        #print(self.client)
        sess= self.client.get_element("{urn:schemas-microsoft-com:xml-analysis}Session")(SessionId=self.sessionId, mustUnderstand = 1)
        self._soapheaders={"Session":sess}
        
    def EndSession(self):
        if self.sessionId is not None:
            nsmap={None:"urn:schemas-microsoft-com:xml-analysis"}
            es= self.client.get_element("{urn:schemas-microsoft-com:xml-analysis}EndSession")(SessionId=self.sessionId, mustUnderstand = 1)
            cmd = etree.Element("{urn:schemas-microsoft-com:xml-analysis}Statement", nsmap=nsmap)
            self.service.Execute(Command=cmd, _soapheaders={"EndSession":es})
            self.setSessionId(None)
            self._soapheaders=None

                
XMLAConnection.setupMembers()
