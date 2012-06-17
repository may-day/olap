'''
Created on 18.04.2012

@author: norman
'''
from zope.interface import implements
from olap.interfaces import IProvider
from olap.xmla.interfaces import IConnection, IXMLADataSource
from suds.client import Client
import http
import types
from pkg_resources import ResourceManager
rm = ResourceManager()
defaultwsdl = "file://"+rm.resource_filename(__name__, "vs.wsdl")

from suds.plugin import MessagePlugin

# the following along with changes to the wsdl (elementFormDefault="unqualified") is needed
# to make it fly with icCube, which expects elements w/o namespace prefix
class UseDefaultNamespace(MessagePlugin):
    def marshalled(self, context):
        for d in context.envelope.getChild('Body').children:
            d.prefix = None
            d.set("xmlns", "urn:schemas-microsoft-com:xml-analysis")

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)

UnmarshallableType=(types.NoneType, types.StringTypes, types.IntType, types.LongType, types.FloatType, types.BooleanType)

def aslist(something):
    """If something is not a list already make it one, otherwise simply return something"""
    return something if isinstance(something, list) else [something]

def listify(result):
    data = aslist(result)
        
    res = []
    for row in data:
        if isinstance(row, UnmarshallableType):
            prop=row
        else:
            prop = {}
            for (k, v) in row:
                if not isinstance(v, UnmarshallableType):
                    v=listify(v)
                prop[k] = v 
        res.append(prop)
    return res

def mapify(result, keyname):
    erg = listify(result)
    res = {}
    for  elem in erg: res[elem[keyname]] = elem
    return res
    
class XMLAProvider(object):
    
    implements(IProvider)
    
    def connect(self, url=defaultwsdl, location=None, username=None, password=None, spn=None, sslverify=True):
        return XMLAConnection(url, location, username, password, spn, sslverify)
    
class XMLADataSource(object):
    
    implements(IXMLADataSource)
    
    def __init__(self, name, desc, url, info, provider, providertype, authmode):
        self.dataSourceName = name
        self.dataSourceDescription=desc
        self.url = url
        self.dataSourceInfo = info
        self.providerName = provider
        self.providerType = aslist(providertype)
        self.authenticationMode = authmode
        
    def __repr__(self):
        return "<XMLADataSource(%s)>" % str(self.__dict__)

xmla1_1_rowsets = {"DISCOVER_DATASOURCES":"",
                   "DISCOVER_PROPERTIES":"PropertyName", 
                   "DISCOVER_SCHEMA_ROWSETS":"SchemaName",
                   "DISCOVER_ENUMERATORS":"",
                   "DISCOVER_LITERALS":"",
                   "DISCOVER_KEYWORDS":"",
                   "DBSCHEMA_CATALOGS":"CATALOG_NAME",
                   "DBSCHEMA_COLUMNS":"",
                   "DBSCHEMA_TABLES":"",
                   "DBSCHEMA_TABLES_INFO":"",
                   "DBSCHEMA_PROVIDER_TYPES":"TYPE_NAME",
                   "MDSCHEMA_ACTIONS":"",
                   "MDSCHEMA_CUBES":"",
                   "MDSCHEMA_DIMENSIONS":"",
                   "MDSCHEMA_FUNCTIONS":"",
                   "MDSCHEMA_HIERARCHIES":"",
                   "MDSCHEMA_MEASURES":"",
                   "MDSCHEMA_MEMBERS":"",
                   "MDSCHEMA_PROPERTIES":"",
                   "MDSCHEMA_SETS":""
                   }
def schemaNameToMethodName(schemaName):
    """
    Convert a schema name like DISCOVER_SCHEMA_ROWSETS into a method name like getSchemaRowsets.
    1. split into parts by _
    2. replace: 
        DBSCHEMA => DBSchema 
        MDSCHEMA => MDSchema
        DISCOVER =>
        otherwise => lower case + capitalize
    3. join results and prepend with "get"
    """
    parts = schemaName.split("_")
    def replace(what):
       
        if what == "DBSCHEMA": return "DBSchema"
        elif what == "MDSCHEMA": return "MDSchema"
        elif what == "DISCOVER": return ""
            
        return what.lower().capitalize()

    return "get" + "".join(map(replace, parts))
            
class XMLAConnection(object):
    
    implements(IConnection)
    
    @classmethod
    def addMethod(cls, funcname, func):
        return setattr(cls, funcname, types.MethodType(func, None, cls))

        
    @classmethod
    def setupMembers(cls):
        def getFunc(schemaName, keyname):
            return lambda this, *args, **kw: cls.Discover(this, schemaName, keyname, *args, **kw)
        
        for schemaName, keyname in xmla1_1_rowsets.items():
            mname = schemaNameToMethodName(schemaName)
            cls.addMethod( mname, getFunc(schemaName, keyname) )

    def __init__(self, url, location, username, password, spn, sslverify):
        if password is None:
            transport = http.HttpKerberosAuthenticated(as_user=username, spn=spn, sslverify=sslverify)
        else:
            transport = http.HttpAuthenticated(username=username, password=password, sslverify=sslverify)
        self.client = Client(url, location=location, transport=transport, cache=None, plugins=[UseDefaultNamespace()])
        
        # optional, call might fail
        self.getMDSchemaLevels = lambda *args, **kw: self.Discover("MDSCHEMA_LEVELS", None, *args, **kw)
        self.sessionid = None
             
        
    def Discover(self, what, keyname=None, restrictions=None, properties=None):
        rl = None
        pl = None
        if restrictions:
            rl = {"RestrictionList":restrictions}
        if properties:
            pl = {"PropertyList":properties}
            
        res = getattr(self.client.service.Discover(what, rl, pl).DiscoverResponse["return"].root, "row", [])
        if res:
            if keyname:
                res = mapify(res, keyname)
            else:
                res = listify(res)
        return res


    def Execute(self, command, dimformat="Multidimensional", axisFormat="TupleFormat", **kwargs):
        if isinstance(command, types.StringTypes):
            command = {"Statement":command}
        props = {"Format":dimformat, "AxisFormat":axisFormat}
        props.update(kwargs)
        pl = {"PropertyList":props}
        return TupleFormatReader(self.client.service.Execute(command, pl).ExecuteResponse["return"].root)
        
    def BeginSession(self):
        bs= self.client.factory.create("BeginSession")
        bs._mustUnderstand = 1
        sess= self.client.factory.create("Session")
        sess._mustUnderstand = 1
        self.client.set_options(soapheaders={"BeginSession":bs})
        self.client.service.Execute({"Statement":None})
        self.sessionid = sess._SessionId=self.client.last_received().childAtPath("/Envelope/Header/Session").getAttribute("SessionId").getValue()
        self.client.set_options(soapheaders=sess)
        
    def EndSession(self):
        if self.sessionid is not None:
            es= self.client.factory.create("EndSession")
            es._mustUnderstand = 1
            es._SessionId = self.sessionid
            self.client.set_options(soapheaders={"EndSession":es})
            self.client.service.Execute({"Statement":None})
            self.sessionid = None
            self.client.set_options(soapheaders=None)

class TupleFormatReader(object):
    
    def __init__(self, tupleresult):
        self.root = tupleresult
        self.cellmap = self.mapOrdinalsToCells()
        
    def mapOrdinalsToCells(self):
        "Return a dict mapping ordinals to cells"
        m = {}
        for cell in listify(getattr(self.root.CellData, "Cell", [])): # "getattr" for the case where there are no cells
            m[int(cell["_CellOrdinal"])] = cell
            
        return m
    
    def getCellByOrdinal(self, ordinal):
        return self.cellmap.get(ordinal, {})
    
    def getAxisTuple(self, axis):
        """Returns the tuple on axis with name <axis>, usually 'Axis0', 'Axis1', 'SlicerAxis'.
        If axis is a number return tuples on the <axis>-th axis."""
        if isinstance(axis, int):
            ax = self.root.Axes.Axis[axis]
        else:
            ax = filter(lambda x: x._name == axis, aslist(self.root.Axes.Axis))[0]
        res = []
        for tup in aslist(getattr(ax.Tuples, "Tuple", [])):
            res.append(listify(tup.Member))
        return res
        
    def getSlice(self, property=None, **kw):
        """
        getSlice(property=None [,Axis<Number>=n|Axis<Number>=[i1,i2,..,ix]])
        
        Return the resulting cells from a MDX statement. The result is presented as an array of arrays of arrays of... depending on amount of axes in the MDX.
        You can carve out slices you need by listing the indices of the axes you are interested in.
        Examples:
        
        result.getSlice() # return all
        result.getSlice(Axis0=3) # carve out the 4th column
        result.getSlice(Axis0=3, SlicerAxis=0) # same as above, SlicerAxis is ignored
        result.getSlice(Axis1=[1,2]) # return the data sliced at the 2nd and 3rd row
        result.getSlice(Axis0=3, Axis1=[1,2]) # return the data sliced at the 2nd and 3rd row in addition to the 4th column 
        
        If you do not want the whole cell returned but just a single property of it (like the Value) name that property in the property parameter:
        
        result.getSlice(property="Value") # from all the cells just get me the Value property
        
        """
        axisranges = [] # list per axis the element indices to include
        
        #n.b: this assumes, axis are listed from Axis0,...AxisN in the ExecuteResponse, 
        #otherwise the ordinal values would be useless anyway
        
        # at this offset we find the first requested index of the dimension
        firstindexoffset = 3
        hyperelemcount=1
        
        for ax in aslist(self.root.Axes.Axis):
            
            if ax._name in kw and ax._name != "SlicerAxis":
                # only include listed indices
                indexrange = kw[ax._name]
                if isinstance(indexrange, int):
                    indexrange = [indexrange]
            else:
                # include all possible indices
                indexrange=range(len(getattr(ax.Tuples, "Tuple", [])))
            if not indexrange:
                if ax._name != "SlicerAxis":
                    # we have requested an empty set from an axis
                    # this renders the whole result empty
                    # it could also because there was an empty set on an axis (i.e. "select {} on columns, [measure].members on rows from [some cube]")
                    # anyway, we can simply stop here an return []
                    return []
                else:
                    # the SlicerAxis could indeed be empty if all dimensions were used on the axes
                    # so we add a dummy entry since this is where the finally result is expected
                    indexrange=[0]
                    
            # first element is a helper to calc the ordinal value from a cell's coord, second is the iteration index
            indexrange = [hyperelemcount, firstindexoffset, []] + indexrange
            hyperelemcount = hyperelemcount*len(ax.Tuples.Tuple)
            axisranges.append(indexrange)
            
        lastdimchange = 0
        while lastdimchange < len(axisranges):
            # calc ordinal number of cell
            ordinal = 0
            for axisrange in axisranges:
                idx=axisrange[axisrange[1]]
                hyperelemcount=axisrange[0]
                ordinal = ordinal + idx*hyperelemcount
            #print ordinal
            
            cell = self.getCellByOrdinal(ordinal)
            if property is None:
                axisranges[0][2].append(cell)
            else:
                axisranges[0][2].append(cell.get(property, None))
            
            # advance to next requested element in slice
            lastdimchange=0
            while lastdimchange < len(axisranges):
                axisrange = axisranges[lastdimchange]
                if axisrange[1] < len(axisrange)-1:
                    axisrange[1] = axisrange[1]+1
                    break
                else:
                    axisrange[1] = firstindexoffset
                    
                lastdimchange = lastdimchange+1
                if lastdimchange < len(axisranges):
                    axisranges[lastdimchange][2].append(axisrange[2])
                    axisrange[2] = []
                    
        # as the last dimension is the sliceraxis it has only one member, so we can safely unpack the first element
        # in that element our resulting multidimensional array has been accumulated
        return axisranges[lastdimchange-1][2][0]
                
XMLAConnection.setupMembers()