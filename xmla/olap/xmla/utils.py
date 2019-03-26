import sys
import six
#from suds.sax.text import Text as sudsText
#from suds.sudsobject import Object as sudsObject
from lxml.etree import QName

stringtypes = six.string_types
_UnmarshallableType=(type(None), six.string_types, six.integer_types, float, bool)
u=six.u

class Data: pass


def aslist(something):
    """If something is not a list already make it one, otherwise simply return something"""
    return something if isinstance(something, list) else [something]

def dictify(r):

    if isinstance(r, list):
        return [dictify(x) for x in r]
    if isinstance(r, Data):
        d = {}
        for (k,v) in r.__dict__.items():
            if k == "text" and v is None: continue
            d[k] = dictify(v)
        return d
    # if isinstance(r, sudsObject):
    #     d = {}
    #     for (k, v) in r:
    #         d[k] = dictify(v)
    #     return d
    if isinstance(r, dict):
        d = {}
        for (k,v) in r.items():
            d[k] = dictify(v)
        return d
    # if isinstance(r, sudsText):
    #     return six.u(r)
    return r


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
            

class PropDict(dict):
    def __getattribute__(self, name):
        try:
            value = self[name]
        except:
            return dict.__getattribute__(self, name)
        if isinstance(value, dict):
            value = PropDict(value)
            self[name] = value
            return value
        elif isinstance(value, list):
            value = [PropDict(x) for x in value]
            self[name] = value
            return value
        return value

    def __delattr__(self, name):
        try:
            value = self[name]
            del self[name]
        except:
            super(PropDict,self).__delattr__(name)
        #try:
        #    value = self[name]
        #    super(PropDict,self).__delattr__(name)
        #except:
        #    super(PropDict,self).__delattr__(name)

def fromETree(e, ns="urn:schemas-microsoft-com:xml-analysis:mddataset"):
    p = Data()
    nst = "{{{}}}*".format(ns)
    valtype = "{http://www.w3.org/2001/XMLSchema-instance}type"
    for (k,v) in e.attrib.items():
        setattr(p, "_"+k, v)
    p.text = e.text
    if p.text and p.text.strip() == "":
        p.text=None
    if valtype in e.attrib:
        if e.attrib[valtype] == "xsd:int":
          p.text = int(p.text)  
          delattr(p, "_"+valtype)
        if e.attrib[valtype] == "xsd:double":
          p.text = float(p.text)  
          delattr(p, "_"+valtype)
        if e.attrib[valtype] == "xsd:float":
          p.text = float(p.text)  
          delattr(p, "_"+valtype)
    for c in e.findall(nst):
        t = QName(c)
        cd = fromETree(c, ns)
        if len(cd.__dict__) == 1:
            cd = cd.text
        v = getattr(p, t.localname, None)
        if v is not None:
            if not isinstance(v, list):
                setattr(p, t.localname, [v])
            getattr(p, t.localname).append(cd)
        else:
            setattr(p, t.localname, cd)
    return p