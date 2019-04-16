import zope.interface
from .interfaces import IXMLASource, schemaElementTypes, SchemaElementNotFound
from .connection import XMLAConnection
import olap.interfaces as ooi
from .utils import u

from pkg_resources import ResourceManager
rm = ResourceManager()
defaultwsdl = "file://"+rm.resource_filename(__name__, "vs.wsdl")



class TREE_OP(object):
    CHILDREN = 0x01
    SIBLINGS = 0x02
    PARENT = 0x04
    SELF = 0x08
    DESCENDANTS = 0x10
    ANCESTORS = 0x20
    
@zope.interface.implementer(ooi.IProvider)
class XMLAProvider(object):
    
    
    def connect(self, url=defaultwsdl, location=None, sslverify=True, **kwargs):
        return XMLASource(url, location, sslverify, **kwargs)


@zope.interface.implementer(ooi.IOLAPSchemaElement)
class XMLAClass(object):

    def __init__(self, unique_name_property, properties, schemaElementName, conn):
        self._properties = properties
        self._conn = conn
        self.unique_name_property = unique_name_property
        self.schemaElementName = schemaElementName

    def __str__(self):
        return self.__class__.__name__ + ":" + str(self.getElementProperties())
    def __repr__(self):
        un = self._properties.get(self.unique_name_property, "???")
        return self.__class__.__name__ + "<" + un + ">"

    def getElementProperties(self):
        return self._properties

    def __getattr__(self, name):
        #print("__getattr__", name)
        #if name == "_properties":
        #    return object.__getattribute__(self, name)
        #print(self._properties)
        if name in self._properties:
            return self._properties[name]
        #print(name, "not in self._properties" )
        return object.__getattr__(self, name)

    def getUniqueName(self):
        if hasattr(self, self.unique_name_property):
            return u("")+getattr(self, self.unique_name_property)
        return None

    def objectfactory(self, clazzname, unp, schemaElementName, props):
        clazz = globals()[clazzname]
        return [clazz(unp, prop, schemaElementName, self._conn) for prop in props]

    def getSchemaElements(self, schemaElementName, unique_name, 
                          aslist=False, more_restrictions=None, 
                          more_properties=None,
                          generate_instance=True):
        types = schemaElementTypes
        et = types[schemaElementName]
        
        r=restrictions = {}
        for otherRestrict in et["RESTRICT_ON"]:
            oet=types[otherRestrict]
            rn=oet["RESTRICTION_NAME"]
            try:
                #print("get current value to restrict on {} by using value of attribute {}".format(otherRestrict, rn))
                r[rn] = getattr(self, rn)
                #print("will restrict on {}={}".format(rn, r[rn]))
            except AttributeError:
                #print("failed getting value of attribute {}".format(rn))
                if more_restrictions and rn in more_restrictions:
                    r[rn] = more_restrictions[rn]
                else:
                    raise
            except:
                #print("failed getting value of attribute {}".format(rn))
                #print(dir(self))
                raise
        if unique_name:
            r[et["RESTRICTION_NAME"]] = unique_name

        if more_restrictions:
            r.update(more_restrictions)

        cat_rn = types["CATALOG"]["RESTRICTION_NAME"]
        try:
            properties= {"Catalog":getattr(self, cat_rn)} 
        except:
            properties = {}

        if more_properties:
            properties.update(more_properties)

        # if there is more than just a CATALOG_NAME in the restrictions
        # we move the catalog to the properties instead
        if cat_rn in r and len(r)>1:
            properties["Catalog"] = r.pop(cat_rn)

        func = getattr(self._conn, et["XMLA_FUNC"])
        props = func(r, properties)

        if props is None or len(props) == 0:
            raise SchemaElementNotFound(r, properties)

        if generate_instance:
            result = self.objectfactory(et["ELEMENT_CLASS"], 
                                      et["PROPERTY_NAME"], 
                                      schemaElementName,
                                      props) 
        else:
            result = props

        if not aslist:
            result = result[0]
        return result

    def query(self, mdx_stmt):
        return self._conn.Execute(mdx_stmt, Catalog=self.CATALOG_NAME)

@zope.interface.implementer(IXMLASource, ooi.IOLAPSource, ooi.IConnection)
class XMLASource(XMLAConnection, XMLAClass):

    def __init__(self, urlwsdl=defaultwsdl, 
                 location=None, 
                 sslverify=True, **kwargs):
        self.urlwsdl=urlwsdl
        self.location=location
        self.sslverify=sslverify
            
        XMLAClass.__init__(self, None, {}, None, self)
        XMLAConnection.__init__(self, urlwsdl, location, sslverify, **kwargs)

    # IConnection interface
    def getOLAPSource(self):
        return self

    # IOLAPSource interface
    def getCatalogs(self):
        """Returns a list of catalogs in the Datasource."""
        return self.getCatalog(None)

    def getCatalog(self, unique_name):
        return self.getSchemaElements("CATALOG", unique_name,
                                      aslist=unique_name==None)

@zope.interface.implementer(ooi.ICatalog)
class XMLACatalog(XMLAClass):
    
    def getCubes(self):
        return self.getCube(None)

    def getCube(self, unique_name):
        return self.getSchemaElements("CUBE", unique_name,
                                      aslist=unique_name==None)

    def getDimensions(self, unique_name=None):
        return self.getSchemaElements("CATALOG_DIMENSION", unique_name, aslist=True)

    def getDimension(self, unique_name):
        return self.getSchemaElements("CATALOG_DIMENSION", unique_name,
                                      aslist=unique_name==None)
    def getHierarchies(self, unique_name=None):
        return self.getSchemaElements("CATALOG_HIERARCHY", unique_name, aslist=True)

    def getHierarchy(self, unique_name=None):
        return self.getSchemaElements("CATALOG_HIERARCHY", unique_name,
                                      aslist=unique_name==None)
    def getSets(self, unique_name=None):
        return self.getSchemaElements("CATALOG_SET", unique_name, aslist=True)

    def getSet(self, unique_name=None):
        return self.getSchemaElements("CATALOG_SET", unique_name,
                                      aslist=unique_name==None)
    def getMeasures(self, unique_name=None):
        return self.getSchemaElements("CATALOG_MEASURE", unique_name, aslist=True)

    def getMeasure(self, unique_name):
        return self.getSchemaElements("CATALOG_MEASURE", unique_name,
                                      aslist=unique_name==None)
@zope.interface.implementer(ooi.ICube)
class XMLACube(XMLAClass):

    def getHierarchies(self):
        return self.getHierarchy(None)

    def getHierarchy(self, unique_name):
        #print("getting hier", unique_name)
        return self.getSchemaElements("HIERARCHY", unique_name, 
                                      aslist=unique_name==None)

    def getMeasures(self):
        return self.getMeasure(None)

    def getMeasure(self, unique_name):
        return self.getSchemaElements("MEASURE", unique_name, 
                                      aslist=unique_name==None)

    def getSets(self):
        return self.getSet(None)

    def getSet(self, unique_name):
        return self.getSchemaElements("SET", unique_name,
                                      aslist=unique_name==None)

    def getDimensions(self):
        return self.getDimension(None)

    def getDimension(self, unique_name):
        return self.getSchemaElements("DIMENSION", unique_name,
                                      aslist=unique_name==None)


@zope.interface.implementer(ooi.IHierarchy)
class XMLAHierarchy(XMLAClass):

    def getLevels(self):
        return self.getLevel(None)

    def getLevel(self, unique_name):
        return self.getSchemaElements("LEVEL", unique_name,
                                      aslist=unique_name==None)
    def getMembers(self):
        return self.getMember(None)

    def getMember(self, unique_name):
        return self.getSchemaElements("HIERARCHY_MEMBER", unique_name,
                                      aslist=unique_name==None)


@zope.interface.implementer(ooi.ILevel)
class XMLALevel(XMLAClass):

    def getMembers(self):
        return self.getMember(None)

    def getMember(self, unique_name):
        return self.getSchemaElements("MEMBER", unique_name,
                                      aslist=unique_name==None)

    def getProperties(self):
        return self.getProperty(None)

    def getProperty(self, unique_name):
        return self.getSchemaElements("PROPERTY", unique_name,
                                      aslist=unique_name==None)

@zope.interface.implementer(ooi.IMember)
class XMLAMember(XMLAClass):

    def getParent(self):
        """Return this members parent member or None if this is the root
        already."""
        pn=self.getParentName()
        if pn:
            return self.getSchemaElements("TREE_MEMBER", 
                                          pn,
                                          aslist=False)
        
        return None

    def getParentName(self):
        """Return this members parent member unique name or None if this is the root
        already."""
        return self.PARENT_UNIQUE_NAME if int(self.PARENT_COUNT) > 0 else None

    def getChildren(self):
        """Return this members children in a list."""
        return self.getSchemaElements("TREE_MEMBER", 
                                      self.getUniqueName(),
                                      aslist=True, 
                                      more_restrictions={"TREE_OP":TREE_OP.CHILDREN})
    def hasChildren(self):
        """Returns True if this member has children False otherwise."""
        return int(self.CHILDREN_CARDINALITY)>0

    def getSiblings(self):
        """Return this members siblings in a list (self is not included)."""
        return self.getSchemaElements("TREE_MEMBER", 
                                      self.getUniqueName(),
                                      aslist=True, 
                                      more_restrictions={"TREE_OP":TREE_OP.SIBLINGS})
    def hasSiblings(self):
        """Returns True if this member has siblings False otherwise."""
        p = self.getParent()
        if p:
            return int(p.CHILDREN_CARDINALITY)>1
        return len(self.getSiblings())>0

    def getAncestors(self):
        """Return the members line of ancestors in a list (self not included)."""
        return self.getSchemaElements("TREE_MEMBER", 
                                      self.getUniqueName(),
                                      aslist=True, 
                                      more_restrictions={"TREE_OP":TREE_OP.ANCESTORS})

@zope.interface.implementer(ooi.IMeasure)
class XMLAMeasure(XMLAClass): pass

@zope.interface.implementer(ooi.IProperty)
class XMLAProperty(XMLAClass): pass

@zope.interface.implementer(ooi.ISet)
class XMLASet(XMLAClass): pass

@zope.interface.implementer(ooi.IDimension)
class XMLADimension(XMLAClass):

    def getHierarchies(self):
        return self.getHierarchy(None)

    def getHierarchy(self, unique_name):
        return self.getSchemaElements("DIMENSION_HIERARCHY", unique_name, 
                                      aslist=unique_name==None)
    def getMembers(self):
        return self.getMember(None)

    def getMember(self, unique_name):
        return self.getSchemaElements("CUBE_DIMENSION_MEMBER", unique_name,
                                      aslist=unique_name==None)


#root.x().getCatalog("FoodMart").getCube("Sales").getHierarchy("[Customers]").getLevel("[Customers].[Country]").getMembers()
#root.x().getCatalog("FoodMart").getCube("HR").getHierarchy("[Employees]").getLevel("[Employees].[Employee Id]").getProperty("Marital Status")._properties
