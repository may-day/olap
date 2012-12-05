olap.rest
=========

This package provides a REST interface to an object providing an IOLAPSource 
or IXMLASource interface.

Example usage
=============

A mini program exposing two interfaces:

```python
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import JSONP
import olap.rest.pyramid as orest
import olap.interfaces as oi
import olap.xmla.xmla as xmla
import cornice

@orest.restify()
class ExposeAll(orest.OLAPREST):
    """All connections can be used by supplying a different name to the datasource,
    i.e. either "mondrian@localhost" or "mondrian2".
    """
    pass

@orest.restify()
class SomeFixed(orest.OLAPREST):
    """
    Here datasource, catalog and cube are fixed. In exposed rest interface the
    corresponding path elements are dropped, i.e.
    "/datasource/mondrian@localhost/catalog/FoodMart/cube/Sales/dimensions" 
    becomes
    "/dimensions" 
    You can enforce the exposure of the whole path by decorating the class like this
    @orest.restify(exposefully=True)
    class SomeFixed(orest.OLAPREST): ...
    """
    DATASOURCE="mondrian@localhost"
    CATALOG="FoodMart"
    CUBE="Sales"


def reg_fixed(config):
    SomeFixed.register_service(config)

def reg_all(config):
    ExposeAll.register_service(config)

def main():
    config = Configurator()

    config.begin()
    config.add_renderer('jsonp', JSONP(param_name="callback"))

    reg = config.registry
    reg.registerUtility(xmla.XMLASource(location = "http://localhost:8080/mondrian/xmla"),
                        oi.IOLAPSource, "mondrian@localhost")
    reg.registerUtility(xmla.XMLASource(location = "http://localhost:8080/mondrian/xmla"),
                        oi.IOLAPSource, "mondrian2")

    cornice.includeme(config)
    # mount them on different paths
    config.include(reg_all, route_prefix="/all")
    config.include(reg_fixed, route_prefix="/fixed")

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

if __name__ == '__main__':
    main()
```

The interface
=============

The following interface is exposed:

* **`(GET) /datasources`**

* **`(GET) /datasource/{ds}`**

>  Return information of the OLAP connection known in the backend.

* **`(GET) /datasource/{ds}/catalogs`**

* **`(GET) /datasource/{ds}/catalog/{cat}`**

>  Retrieve information about the catalogs in a datasource.
  
* **`(GET) /datasource/{ds}/catalog/{cat}/sets`**

* **`(GET) /datasource/{ds}/catalog/{cat}/set/{set}`**

> Retrieve information about the sets  in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/hierarchies`**

* **`(GET) /datasource/{ds}/catalog/{cat}/hierarchy/{huname}`**

> Retrieve information about the hierarchies in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/measures`**

* **`(GET) /datasource/{ds}/catalog/{cat}/measure/{muname}`**

> Retrieve information about the measures in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/queries`**

> Return all queries with attached results currently in the session cache.

* **`(POST) /datasource/{ds}/catalog/{cat}/queries`**

> Create a new query, execute it and return its result along with a query id.
> The query is expected in a `mdx` property.

* **`(GET) /datasource/{ds}/catalog/{cat}/query/{qid}`**

> Return results of a query if still in session cache.

* **`(GET) /datasource/{ds}/catalog/{cat}/dimensions`**

* **`(GET) /datasource/{ds}/catalog/{cat}/dimension/{duname}`**

> Retrieve information about the dimensions in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/dimension/{duname}/members`**

* **`(GET) /datasource/{ds}/catalog/{cat}/dimension/{duname}/member/{muname}`**

> Retrieve information about the members of a dimension in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/cubes`**

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}`**

> Retrieve information about the cubes in a catalog.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/sets`**

> Return information about all sets in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/set/{set}`**

> Return information about a set in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/measures`**

> Return information about all measures in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/measure/{muname}`**

> Return information about a measure in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/dimensions`**

> Return information about all dimensions in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/dimension/{duname}`**

> Return information about a dimension in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchies`**

> Return information about all hierarchies in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}`**

> Return information about a hierarchy in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/members`**

> Return information about all members of a hierarchy in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/member/{muname}`**

> Return information about a member of a hierarchy in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/levels`**

> Return information about all levels of a hierarchy in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/level/{luname}`**

> Return information about a level of a hierarchy in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/level/{luname}/members`**

> Return information about all members of a hierarchy's level in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/level/{luname}/member/{muname}`**

> Return information about a member of a hierarchy's level in a cube.


* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/dimension/{duname}/members`**

> Return information about all members of a dimension in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/dimension/{duname}/member/{muname}`**

> Return information about a member of a dimension in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/member/{muname}/children`**

> Return information about the children of a hierarchy's member in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/level/{luname}/properties`**

> Return information about all properties of a hierarchy's level in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/level/{luname}/property/{pname}`**

> Return information about a property of a hierarchy's level in a cube.

* **`(GET) /datasource/{ds}/catalog/{cat}/cube/{cube}/hierarchy/{huname}/member/{muname}/existingchildren`**

> Return information about the NON EMPTY children of a hierarchy's member in a cube w.r.t. a
> second set specified in the query string parameter called `set2`.

PATH parameter:

* **`ds`**
    the name that was used to register the connection as an utility
* **`cat`**
    a catalog name
* **`cube`**
    a cube name
* **`duname`**
    the unique name of a dimension
* **`huname`**
    the unique name of a hierarchy
* **`luname`**
    the unique name of a level
* **`muname`**
    the unique name of a member
* **`pname`**
    a property name
* **`qid`**
    the query id as returned when a query is created
