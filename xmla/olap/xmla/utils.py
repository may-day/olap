import types
from suds.sax.text import Text as sudsText
from suds.sudsobject import Object as sudsObject

_UnmarshallableType=(types.NoneType, types.StringTypes, types.IntType, 
                    types.LongType, types.FloatType, types.BooleanType)


def aslist(something):
    """If something is not a list already make it one, otherwise simply return something"""
    return something if isinstance(something, list) else [something]

def dictify(r):

    if isinstance(r, list):
        return [dictify(x) for x in r]
    if isinstance(r, sudsObject):
        d = {}
        for (k, v) in r:
            d[k] = dictify(v)
        return d
    if isinstance(r, sudsText):
        return unicode(r)
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
