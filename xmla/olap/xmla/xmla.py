import zope.interface
from connection import XMLAConnection
import olap.xmla.interfaces as oxi
import olap.interfaces as ooi

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
    

class XMLAProvider(object):
    
    zope.interface.implements(ooi.IProvider)
    
    def connect(self, url=defaultwsdl, location=None, username=None, 
                password=None, spn=None, sslverify=True):
        return XMLASource(url, location, username, password, spn, sslverify)


class XMLAClass(object):
    zope.interface.implements(ooi.IOLAPSchemaElement)

    def __init__(self, unique_name_property, properties, schemaElementName, conn):
        self._properties = properties
        self._conn = conn
        self.unique_name_property = unique_name_property
        self.schemaElementName = schemaElementName

    def __str__(self):
        return self.__class__.__name__ + ":" + str(self.getElementProperties())

    def getElementProperties(self):
        return self._properties

    def __getattribute__(self, name):
        if name == "_properties":
            return object.__getattribute__(self, name)
        elif name in self._properties:
            return self._properties[name]
        return object.__getattribute__(self, name)

    def getUniqueName(self):
        if hasattr(self, self.unique_name_property):
            return u""+getattr(self, self.unique_name_property)
        return None

    def objectfactory(self, clazzname, unp, schemaElementName, props):
        clazz = globals()[clazzname]
        return [clazz(unp, prop, schemaElementName, self._conn) for prop in props]

    def getSchemaElements(self, schemaElementName, unique_name, 
                          aslist=False, more_restrictions=None, 
                          more_properties=None,
                          generate_instance=True):
        types = oxi.schemaElementTypes
        et = types[schemaElementName]
        
        r=restrictions = {}
        for otherRestrict in et["RESTRICT_ON"]:
            oet=types[otherRestrict]
            rn=oet["RESTRICTION_NAME"]
            try:
                r[rn] = getattr(self, rn)
            except AttributeError:
                if more_restrictions and rn in more_restrictions:
                    r[rn] = more_restrictions[rn]
                else:
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
            raise oxi.SchemaElementNotFound(r, properties)

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

class XMLASource(XMLAConnection, XMLAClass):
    zope.interface.implements(oxi.IXMLASource, ooi.IOLAPSource, ooi.IConnection)


    def __init__(self, urlwsdl=defaultwsdl, 
                 location=None, username=None, password=None, spn=None,
                 sslverify=True):
        self.urlwsdl=urlwsdl
        self.location=location
        self.username=username
        self.password=password
        self.spn=spn
        self.sslverify=sslverify
            
        XMLAClass.__init__(self, None, {}, None, self)
        XMLAConnection.__init__(self, urlwsdl, location, username, 
                                           password, spn, sslverify)

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

class XMLACatalog(XMLAClass):
    zope.interface.implements(ooi.ICatalog)
    
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
class XMLACube(XMLAClass):
    zope.interface.implements(ooi.ICube)

    def getHierarchies(self):
        return self.getHierarchy(None)

    def getHierarchy(self, unique_name):
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


class XMLAHierarchy(XMLAClass):
    zope.interface.implements(ooi.IHierarchy)

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


class XMLALevel(XMLAClass):
    zope.interface.implements(ooi.ILevel)

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

class XMLAMember(XMLAClass):
    zope.interface.implements(ooi.IMember)

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

class XMLAMeasure(XMLAClass):
    zope.interface.implements(ooi.IMeasure)

class XMLAProperty(XMLAClass):
    zope.interface.implements(ooi.IProperty)

class XMLASet(XMLAClass):
    zope.interface.implements(ooi.ISet)

class XMLADimension(XMLAClass):
    zope.interface.implements(ooi.IDimension)

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
