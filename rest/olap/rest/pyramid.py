import zope.component
import olap.interfaces as oi
import olap.xmla.interfaces as oxi
import olap.xmla.utils as utils
from olap.xmla.xmla import TREE_OP
import uuid

from cornice.resource import resource
from cornice.service import Service
import cornice.pyramidhook

from webob import Response, exc
import json
import logging
import functools
from types import MethodType

try:
    import venusian
    VENUSIAN = True
except ImportError:
    VENUSIAN = False

logger = logging.getLogger(__name__)

class _404(exc.HTTPError):
    def __init__(self, msg='Not Found'):
        body = {'status': 404, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 404
        self.content_type = 'application/json'

class _502(exc.HTTPError):
    def __init__(self, msg='Bad Gateway'):
        body = {'status': 502, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 502
        self.content_type = 'application/json'

doc={
"DATASOURCE":"""
Retrieve information about the datasources available, i.e. those that are 
available as utilities and providing the IOLAPSource interface.
""",
"DATASOURCE_coll_get":"""
Return information about all datasources.
""",
"DATASOURCE_single_get":"""
Return information about a specific datasource identified by the name it
was registered in the pyramid application.
""",
"CATALOG":"""
Retrieve information about the catalogs in a datasource.
""",
"CATALOG_coll_get":"""
Return information about all catalogs.
""",
"CATALOG_single_get":"""
Return information about a specific catalog identified by its name.
""",
"QUERY":"""
Issue MDX queries and retrieve the result.
""",
"QUERY_single_get":"""
Return result and axes information from a query identified by its ID.
""",
"QUERY_coll_get":"""
Return all cached queries.
""",
"QUERY_single_post":"""
Issue a new MDX query. The answer returned contains the resultset and axes 
information as well as an ID by which the result is cached on the server and
can be retrieved again.
""",
"CUBE":"""
Retrieve information about a cube.
""",
"CUBE_coll_get":"""
Return information about all cubes in a catalog.
""",
"CUBE_single_get":"""
Return information about a specific cube in a catalog identified by its name.
""",
"CATALOG_DIMENSION":"""
Retrieve information about a dimension.
""",
"CATALOG_DIMENSION_coll_get":"""
Return information about all dimensions in a catalog.
""",
"CATALOG_DIMENSION_single_get":"""
Return information about a specific dimension in a catalog identified by its name.
""",
"CATALOG_HIERARCHY":"""
Retrieve information about a hierarchy.
""",
"CATALOG_HIERARCHY_coll_get":"""
Return information about all hierarchies in a catalog.
""",
"CATALOG_HIERARCHY_single_get":"""
Return information about a specific hierarchy in a catalog identified by its name.
This can result in a list of hierarchies if they are used in multiple cubes.
""",
"CATALOG_SET":"""
Retrieve information about a set.
""",
"CATALOG_SET_coll_get":"""
Return information about all sets in a catalog.
""",
"CATALOG_SET_single_get":"""
Return information about a specific set in a catalog identified by its name.
This can result in a list of sets if they are used in multiple cubes.
""",
"CATALOG_MEASURE":"""
Retrieve information about a measure.
""",
"CATALOG_MEASURE_coll_get":"""
Return information about all measures in a catalog.
""",
"CATALOG_MEASURE_single_get":"""
Return information about a specific measure in a catalog identified by its name.
This can result in a list of measures if they are used in multiple cubes.
""",
"DIMENSION":"""
Retrieve information about a dimension.
""",
"DIMENSION_coll_get":"""
Return information about all dimensions in a cube.
""",
"DIMENSION_single_get":"""
Return information about a specific dimension in a cube identified by its name.
""",
"HIERARCHY":"""
Retrieve information about a hierarchy.
""",
"HIERARCHY_coll_get":"""
Return information about all hierarchies in a cube.
""",
"HIERARCHY_single_get":"""
Return information about a specific hierarchy in a cube identified by its name.
""",
"SET":"""
Retrieve information about a set.
""",
"SET_coll_get":"""
Return information about all sets in a cube.
""",
"SET_single_get":"""
Return information about a specific set in a cube identified by its name.
""",
"MEASURE":"""
Retrieve information about a measure.
""",
"MEASURE_coll_get":"""
Return information about all measures in a cube.
""",
"MEASURE_single_get":"""
Return information about a specific measure in a cube identified by its name.
""",
"LEVEL":"""
Retrieve information about a level.
""",
"LEVEL_coll_get":"""
Return information about all level in a hierarchy.
""",
"LEVEL_single_get":"""
Return information about a specific level in a hierarchy identified by its name.
""",
"HIERARCHY_MEMBER":"""
Retrieve information about a member.
""",
"HIERARCHY_MEMBER_coll_get":"""
Return information about all members in a hierarchy.
""",
"HIERARCHY_MEMBER_single_get":"""
Return information about a specific member in a hierarchy identified by its name.
""",
"MEMBER":"""
Retrieve information about a member.
""",
"MEMBER_coll_get":"""
Return information about all members in a level.
""",
"MEMBER_single_get":"""
Return information about a specific member in a level identified by its name.
""",
"PROPERTY":"""
Retrieve information about a property.
""",
"PROPERTY_coll_get":"""
Return information about all properties in a level.
""",
"PROPERTY_single_get":"""
Return information about a specific property in a level identified by its name.
""",
"DIMENSION_MEMBER":"""
Retrieve information about a member.
""",
"DIMENSION_MEMBER_coll_get":"""
Return information about all members in a dimensions.
""",
"DIMENSION_MEMBER_single_get":"""
Return information about a specific member in a dimension identified by its 
name.
""",
"CUBE_DIMENSION_MEMBER":"""
Retrieve information about a member.
""",
"CUBE_DIMENSION_MEMBER_coll_get":"""
Return information about all members in a dimensions of a cube.
""",
"CUBE_DIMENSION_MEMBER_single_get":"""
Return information about a specific member in a dimension of a cube identified
by its name.
"""
}

resourceelements = {
    "DATASOURCE":
        ("datasources", "datasource","ds_name", None),
    "CATALOG":
        ("catalogs", "catalog", "CATALOG_NAME", "DATASOURCE"),
    "QUERY":
        ("queries", "query", "QUERY_ID", "CATALOG"),
    "CUBE":
        ("cubes", "cube", "CUBE_NAME", "CATALOG"),
    "CATALOG_DIMENSION":
        ("dimensions", "dimension", "DIMENSION_UNIQUE_NAME", "CATALOG"), 
    "CATALOG_HIERARCHY":
        ("hierarchies", "hierarchy", "HIERARCHY_UNIQUE_NAME", "CATALOG"),
    "CATALOG_SET":
        ("sets", "set", "SET_NAME", "CATALOG"),
    "CATALOG_MEASURE":
        ("measures", "measure", "MEASURE_UNIQUE_NAME", "CATALOG"),
    "DIMENSION":
        ("dimensions", "dimension", "DIMENSION_UNIQUE_NAME", "CUBE"),
    "HIERARCHY":
        ("hierarchies", "hierarchy", "HIERARCHY_UNIQUE_NAME", "CUBE"),
    "SET":
        ("sets", "set", "SET_NAME", "CUBE"),
    "MEASURE":
        ("measures", "measure", "MEASURE_UNIQUE_NAME", "CUBE"),
    "LEVEL":
        ("levels", "level", "LEVEL_UNIQUE_NAME", "HIERARCHY"),
    "HIERARCHY_MEMBER":
        ("members", "member", "MEMBER_UNIQUE_NAME", "HIERARCHY"),
    "HM_CHILDREN_WRT":
        ("existingchildren", "", "DUMMY", "HIERARCHY_MEMBER"),
    "HM_CHILDREN":
        ("children", "", "DUMMY", "HIERARCHY_MEMBER"),
    "MEMBER":
        ("members", "member", "MEMBER_UNIQUE_NAME", "LEVEL"),
    "PROPERTY":
        ("properties", "property", "PROPERTY_NAME", "LEVEL"),
    "DIMENSION_MEMBER":
        ("members", "member", "MEMBER_UNIQUE_NAME", "CATALOG_DIMENSION"),
    "CUBE_DIMENSION_MEMBER":
        ("members", "member", "MEMBER_UNIQUE_NAME", "DIMENSION"),
    }


def restify(exposefully=False, **kw):
    def wrapper(klass):
        re=resourceelements
        services = {}
        fixedvars = {}
        fixedvalues = {}
        neededvars = {}

        "CATALOG_DIMENSION",  "CATALOG_HIERARCHY", "CATALOG_SET", "CATALOG_MEASURE"

        for schemaElementName, opts in re.items():
            fixedvalue = getattr(klass, schemaElementName, None)
            if fixedvalue:
                fixedvars[schemaElementName] = fixedvalue
                fixedvalues[opts[2]] = fixedvalue

        for schemaElementName, opts in re.items():
            if schemaElementName in fixedvars and not exposefully:
                continue

            if "CUBE" in fixedvars and "CATALOG" and not exposefully \
                    and schemaElementName in ["CATALOG_DIMENSION",  
                                              "CATALOG_HIERARCHY", 
                                              "CATALOG_SET", 
                                              "CATALOG_MEASURE",
                                              "DIMENSION_MEMBER"]:
                continue

            single_invalid = False
            coll_invalid = False
            paramlist = []
            coll_path = single_path = ""
            coll_path, single_path, param, parent_path = opts

            single_invalid = single_invalid or not single_path
            coll_invalid = coll_invalid or not coll_path

            coll_method = [("get" + coll_path.capitalize(), None)]
            single_method = [("get" + single_path.capitalize(), param)]
            paramlist.append(param)

            klass.name_parametername = param
            single_path = single_path + "/{" + param + "}"
            hidden=False
            while parent_path:
                if parent_path in fixedvars and not exposefully:
                    hidden=True
                coll, single, param, parent_path = re[parent_path]
                seq = ("get" + single.capitalize(), param)
                # only in the root can there be a collection requested
                coll_method.insert(0, seq)
                single_method.insert(0, seq)
                paramlist.append(param)

                single_invalid = single_invalid or not single
                coll_invalid = coll_invalid or not single

                if not hidden:
                    coll_path = single+"/{"+param + "}/" + coll_path
                    single_path = single+"/{"+param + "}/" + single_path

            coll_path = "/" + coll_path
            single_path = "/" + single_path
            neededvars[schemaElementName] = paramlist
            #print coll_path
            #print single_path
            
            single_name=schemaElementName + klass.__name__.lower()
            coll_name="collection_"+schemaElementName + klass.__name__.lower()

            servicelist = []
            if not single_invalid: servicelist.append(
                (single_name, single_path, single_method, ""))

            if not coll_invalid: servicelist.append(
                (coll_name, coll_path, coll_method, "collection_"))

            for (n,p,c,prefix) in servicelist:

                dockey = schemaElementName + (prefix and "_coll" or "_single") + "_get"
                desc = doc.get(dockey, "") or klass.__doc__ or klass.__name__
                services[n]=service=Service(name=n, 
                                            path=p, 
                                            description=desc,
                                            renderer="jsonp", 
                                            accept="application/json"
                                            )
                for verb in ("get", "post", "put", "delete", "patch", "options"):
                    methodname=prefix+schemaElementName.lower()+"_"+verb
                    wrappername = "_"+methodname+"_wrapper"
                    if not hasattr(klass, methodname):
                        methodname = prefix+verb
                        if not hasattr(klass, methodname): continue

                    origmethod=getattr(klass, methodname)
                    wrapperfunc=functools.update_wrapper(
                        functools.partial(origmethod, 
                                          schemaElementName=schemaElementName,
                                          callsequence=c),
                        origmethod
                        )
                    method = MethodType( wrapperfunc, None, klass)
                    # can only document on service level
                    #dockey = schemaElementName + (prefix and "_coll" or "_single") + verb
                    #if doc.has_key(dockey):
                    #    setattr(method, "__doc__", doc[dockey])
                    setattr(klass, wrappername, method)
                    service.add_view(verb, wrappername, klass=klass)
        setattr(klass,'_services', services)
        setattr(klass,'fixedvalues', fixedvalues)
        setattr(klass, 'neededvars', neededvars)

        if VENUSIAN:
            def callback(context, name, ob):
                # get the callbacks registred by the inner services
                # and call them from here when the @resource classes are being
                # scanned by venusian.
                for service in services.values():
                    config = context.config.with_package(info.module)
                    config.add_cornice_service(service)

            info = venusian.attach(klass, callback, category='pyramid')

        return klass

    return wrapper

class OLAPREST(object):
    def __init__(self, request):
        self.request = request
        self.kw=self.request.matchdict.copy()
        if self.fixedvalues:
            self.kw.update(self.fixedvalues)
                
        try:
            s = self.request.session
            if "queries" not in s:
                s["queries"] = {}
            self.q = s["queries"]
        except:
            # no session configured
            logger.warning("no sessioning configured!")
            self.q = {} # one-off

    def _serialize(self, name, olap):
        ds = {}
        ds["registered_name"] = name
        ds["location"] = olap.location
        ds["username"] = olap.username
        ds["spn"] = olap.spn
        return ds

    def collection_datasource_get(self, **kw):
        datasources = []
        if "ds_name" in self.fixedvalues:
            name = self.kw["ds_name"]
            if not isinstance(name, basestring):
                name="hidden"
            olap=self.datasource_get()
            datasources.append(self._serialize(name, olap))
            return datasources

        reg = self.request.registry
        for x in reg.getUtilitiesFor(oi.IOLAPSource):
            datasources.append(self._serialize(*x))
        return datasources

    def datasource_get(self, **kw):
        reg = self.request.registry
        name = self.kw["ds_name"]
        try:
            if isinstance(name, basestring):
                olap = reg.getUtility(oi.IOLAPSource, name)
            else:
                olap = name
            return olap
        except zope.component.ComponentLookupError:
            raise _404("An IOLAPSource with name '%s' was not found." % name)

    def collection_get(self, schemaElementName=None, callsequence=None):
        return self.get(schemaElementName=schemaElementName, 
                        callsequence=callsequence, 
                        aslist=True)

    def get_iolap(self, ds, callsequence):
        calls = callsequence
        calls = calls[:]
        calls.pop(0) # the first is the datasource, but we have that already
        lastobj = ds
        while calls:
            methodname, paramname = calls.pop(0)
            params = [] if paramname is None else [self.kw[paramname]]
            lastobj = getattr(lastobj, methodname)(*params)
        listresult = lastobj if isinstance(lastobj, list) else [lastobj]
        return [utils.dictify(e.getElementProperties()) for e in listresult]

    def get(self, schemaElementName=None, callsequence=None, aslist=False, 
            altSchemaElementName=None):
        ds = self.datasource_get()
        self.kw.pop("ds_name")

        # if we ask for, say catalogs, but have also a fixed cube defined
        # we will have the variable for the CUBE in the kw.
        # we have to remove that or the getSchemaElements will bomb
        for k, v in self.fixedvalues.items():
            if k not in self.neededvars[schemaElementName]:
                del self.kw[k]

        try:
            if oxi.IXMLASource.providedBy(ds):
                return utils.dictify(ds.getSchemaElements(
                        altSchemaElementName or schemaElementName, 
                        None, 
                        aslist=aslist, 
                        more_restrictions=self.kw, 
                        generate_instance=False))
            else:
                return self.get_iolap(ds, callsequence)
        except oxi.SchemaElementNotFound, e:
            raise _404({"restrictions:":e.restrictions, "properties":e.properties})
        except oi.OlapException, e:
            msg = {"errormessage":e.message, "errorfault":str(e.detail)}
            raise _502(msg)

    def collection_hm_children_get(self, 
                                   schemaElementName=None, 
                                   callsequence=None, 
                                   aslist=False):

        self.kw["TREE_OP"] = TREE_OP.CHILDREN
        return self.get(schemaElementName=schemaElementName, 
                        callsequence=callsequence, aslist=True,
                        altSchemaElementName="TREE_MEMBER")

    def collection_hm_children_wrt_get(self, 
                                   schemaElementName=None, 
                                   callsequence=None, 
                                   aslist=False):

        set2 = self.request.GET.get("set2", "{}")
#        mg = self.request.GET.get("measuregroup", None)
#        if mg:
#            set2 = set2 + ", " + mg
        ds = self.datasource_get()
        cat = ds.getCatalog(self.kw["CATALOG_NAME"])
        cube = self.kw["CUBE_NAME"]
        member = self.kw["MEMBER_UNIQUE_NAME"] + ".children"
        cmd="SELECT NON EMPTY %s ON COLUMNS, %s on ROWS FROM [%s]" %\
            (member, set2, cube)
        res=cat.query(cmd)
        axistuple = utils.dictify(res.getAxisTuple(0))
        result = []
        for member in res.getAxisTuple(0):
            # in case someone played with MAMBER_UNIQUE_NAME
            #if isinstance(member, list):
            #    member = member[0]
            children = int(member.DisplayInfo) & 0xffff
            m = {}
            m["CHILDREN_CARDINALITY"] = str(children)
            m["MEMBER_CAPTION"] = member.Caption
            m["MEMBER_UNIQUE_NAME"] = member.UName
            m["LEVEL_NUMBER"] = member.LNum
            m["LEVEL_UNIQUE_NAME"] = member.LName
            result.append(m)

        return result
        
    ############################ query related methods #########################
    def collection_query_get(self, schemaElementName=None, callsequence=None):
        return self.q

    def query_get(self, schemaElementName=None, callsequence=None):
        try:
            return self.q[self.kw["QUERY_ID"]]
        except:
            raise _404("No query with ID '%s' found." % self.kw.get("QUERY_ID", "None"))

    def collection_query_post(self, schemaElementName=None, callsequence=None):
        r=self.request.json_body.copy()
        ds = self.datasource_get()
        cat = ds.getCatalog(self.request.matchdict["CATALOG_NAME"])
        res=cat.query(r["mdx"])
        axistuple = []
        try:
            axis=0
            while True:
                axistuple.append(res.getAxisTuple(axis))
                axis += 1
        except:
            pass
        prop = r.get("properties", None)
        slices = res.getSlice(properties=prop)
        uid=str(uuid.uuid4())
        self.q[uid] = utils.dictify({
            "axes" : axistuple,
            "cells" : slices,
            "id" : uid,
            "mdx" : r["mdx"]
            })
        return self.q[uid]

    @classmethod
    def register_service(cls, config):
        for service in cls._services.values():
            cornice.pyramidhook.register_service_views(config, service)

