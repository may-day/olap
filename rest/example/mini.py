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
