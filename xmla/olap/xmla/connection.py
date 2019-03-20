'''
Created on 18.04.2012

@author: norman
'''
from olap.xmla.interfaces import XMLAException
from suds.client import Client
from suds import WebFault
from . import httptransport
import types
from .formatreader import TupleFormatReader
from .utils import *
import logging

logger = logging.getLogger(__name__)

from suds.plugin import MessagePlugin

# the following along with changes to the wsdl (elementFormDefault="unqualified") is needed
# to make it fly with icCube, which expects elements w/o namespace prefix
class UseDefaultNamespace(MessagePlugin):
    def marshalled(self, context):
        for d in context.envelope.getChild('Body').children:
            d.prefix = None
            d.set("xmlns", "urn:schemas-microsoft-com:xml-analysis")

class SessionPlugin(MessagePlugin):
  def __init__(self, xmlaconn):
      self.xmlaconn = xmlaconn

  def parsed(self, context):
      if self.xmlaconn.getListenOnSessionId():
          self.xmlaconn.setSessionId(context.reply.childAtPath("/Envelope/Header/Session").getAttribute("SessionId").getValue())

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

        if password is None:
            transport = httptransport.HttpKerberosAuthenticated(as_user=username, 
                                                       spn=spn, 
                                                       sslverify=sslverify,
                                                       **kwargs)
        else:
            transport = httptransport.HttpAuthenticated(username=username, 
                                               password=password, 
                                               sslverify=sslverify,
                                               **kwargs)
        self.sessionplugin=SessionPlugin(self)
        self.client = Client(url, 
                             location=location, 
                             transport=transport, 
                             cache=None, unwrap=False,
                             plugins=[UseDefaultNamespace(), self.sessionplugin])
        
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
            doc=self.client.service.Discover(what, rl, pl)
            res = getattr(doc.DiscoverResponse["return"].root, "row", [])
            if res:
                res = aslist(res)
        except WebFault as fault:
            raise XMLAException(fault.fault, dictify(fault.fault))
        logger.debug( res )
        return res


    def Execute(self, command, dimformat="Multidimensional", 
                axisFormat="TupleFormat", **kwargs):
        if isinstance(command, stringtypes):
            command = {"Statement":command}
        props = {"Format":dimformat, "AxisFormat":axisFormat}
        props.update(kwargs)
        pl = {"PropertyList":props}
        try:
            root = self.client.service.Execute(command, pl).ExecuteResponse["return"].root
            return TupleFormatReader(root)
        except WebFault as fault:
            raise XMLAException(fault.fault, dictify(fault.fault))
        
        
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
            self.client.service.Execute({"Statement":None})
            self.setSessionId(None)
            self.client.set_options(soapheaders=None)

                
XMLAConnection.setupMembers()
