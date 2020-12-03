import six
from lxml import etree
from lxml.etree import QName

stringtypes = six.string_types
_UnmarshallableType=(type(None), six.string_types, six.integer_types, float, bool)
u=six.u

schema_instance="http://www.w3.org/2001/XMLSchema-instance"
class Data(dict):

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return getattr(super(Data, self), name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


def aslist(something):
    """If something is not a list already make it one, otherwise simply return something"""
    return something if isinstance(something, list) else [something]

def dictify(r, keep_none_text=False):

    if isinstance(r, list):
        return [dictify(x, keep_none_text) for x in r]
    if isinstance(r, Data):
        d = {}
        for (k,v) in r.items():
            if k == "text" and v is None and not keep_none_text: continue
            d[k] = dictify(v, keep_none_text)
        return d
    if isinstance(r, dict):
        d = {}
        for (k,v) in r.items():
            d[k] = dictify(v, keep_none_text)
        return d
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

def etree_tostring(et):
    return etree.tostring(et, pretty_print=True).decode("utf-8")

def as_etree(dict_or_str, parent_if_content=None):

    top = {}
    if isinstance(dict_or_str, stringtypes):
        top = {dict_or_str:None}
    elif isinstance(dict_or_str, dict):
        top = dict_or_str
        if isinstance(parent_if_content, stringtypes) and top:
            top = {parent_if_content:top}

    elems = []
    for (elem_name, elem_value) in top.items():
        
        elem=etree.Element(elem_name)
        if isinstance(elem_value, dict):
            subelem = as_etree(elem_value)
            if subelem is not None:
                if isinstance(subelem, list):
                    for c in subelem:
                        elem.append(c)
                else:
                    elem.append(subelem)
        else:
            if elem_value is not None:
                elem.text = str(elem_value)
        elems.append(elem)

    res = None
    if len(elems)==1:
        res = elems[0]
    elif len(elems)>1:
        res = elems
    return res

def ns_name(ns, name):
    if ns is None:
        return name
    return "{{{}}}{}".format(ns,name)

def fromETree(e, ns):
    p = Data()
    nst = ns_name(ns, "*")
    valtype = ns_name(schema_instance, "type")
    if e is not None:
        for (k,v) in e.attrib.items():
            setattr(p, "_"+k, v)
        p.text = e.text
        if p.text and p.text.strip() == "":
            p.text=None
    else:
        p.text=None
    if e is not None:
        if valtype in e.attrib:
            if e.attrib[valtype] in ["xsd:int", "xsd:unsignedInt"]:
                p.text = int(p.text)  
                delattr(p, "_"+valtype)
            elif e.attrib[valtype] in ["xsd:long"]:
                p.text = int(p.text)  if six.PY3 else long(p.text)
                delattr(p, "_"+valtype)
            elif e.attrib[valtype] in ["xsd:double", "xsd:float"]:
                p.text = float(p.text)  
                delattr(p, "_"+valtype)
        for c in e.findall(nst):
            t = QName(c)
            
            cd = fromETree(c, ns)
            #if len(cd.__dict__) == 1:
            if len(cd) == 1:
                cd = cd.text
            v = getattr(p, t.localname, None)
            if v is not None:
                if not isinstance(v, list):
                    setattr(p, t.localname, [v])
                getattr(p, t.localname).append(cd)
            else:
                setattr(p, t.localname, cd)
    return p