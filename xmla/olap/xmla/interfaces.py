'''
Created on 18.04.2012

@author: norman
'''
#@PydevCodeAnalysisIgnore

from zope.interface import Interface
import zope.schema
#from olap import xmla
import olap.interfaces as ooi
from .utils import u

class XMLAException(ooi.OlapException): pass
class SchemaElementNotFound(Exception):
    def __init__(self, restrictions, properties):
        super(SchemaElementNotFound, self).__init__()
        self.restrictions = restrictions
        self.properties = properties



class IXMLASource(ooi.IOLAPSource):

    urlwsdl = zope.schema.TextLine(
        title=u("WSDL URL"),
        description=u("URL of wsdl defining the XMLA service, leave empty to use default."),
        required=False
        )

    location= zope.schema.TextLine(
        title=u("XMLA Server location"),
        description=u("URL of this XMLA Server"),
        required=True
        )

    sslverify= zope.schema.TextLine(
        title=u("sslverify"),
        description=u("""Verify ssl certificate on ssl connections. 
Leave empty to accept any certifacte or point to a file on this server 
containing a certicate bundle"""),
        required=False
        )

    log= zope.schema.TextLine(
        title=u("log"),
        description=u("""Provide your own instance of a Zeep logging plugin or set to True to use builtin"""),
        required=False
        )

    session= zope.schema.TextLine(
        title=u("session"),
        description=u("""Provide your own session instance to zeep's transport"""),
        required=False
        )

    def getSchemaElements(schemaElementType, unique_name, 
                          aslist=False, more_restrictions=None, 
                          more_properties=None,
                          generate_instance=True):
        """Returns a list of schema elements or a single entry.

        schemaElementType: refers to a key in `schemaElementTypes`
        unique_name: return a specific element
        aslist: return result as list, if false the first in the resultset will be returned
        more_restrictions: dictionary containing more constraints for the request, i.e.
                           {"HIERARCHY_UNIQUE_NAME":"[Sales by Country]"}
        more_properties: dictionary containing more properties for the request,
                           {"ProviderInfo":"YourProvider"}
        generate_instance: If false the resulting entries will be dictionaries, otherwise
                           of the type mentioned in the "ELEMENT_CLASS" entry 
                           from the schemaELementType.
                           """

schemaElementTypes = {
    "CATALOG": {"RESTRICTION_NAME":"CATALOG_NAME",
                "PROPERTY_NAME":"CATALOG_NAME",
                "ELEMENT_CLASS":"XMLACatalog",
                "XMLA_FUNC":"getDBSchemaCatalogs",
                "RESTRICT_ON":[]},
    "CUBE": {"RESTRICTION_NAME":"CUBE_NAME",
             "PROPERTY_NAME":"CUBE_NAME",
             "ELEMENT_CLASS":"XMLACube",
             "XMLA_FUNC":"getMDSchemaCubes",
             "RESTRICT_ON":[]},
    "HIERARCHY": {"RESTRICTION_NAME":"HIERARCHY_UNIQUE_NAME",
                  "PROPERTY_NAME":"HIERARCHY_UNIQUE_NAME",
                  "ELEMENT_CLASS":"XMLAHierarchy",
                  "XMLA_FUNC":"getMDSchemaHierarchies",
                  "RESTRICT_ON":["CUBE"]},
    "DIMENSION_HIERARCHY": {"RESTRICTION_NAME":"HIERARCHY_UNIQUE_NAME",
                            "PROPERTY_NAME":"HIERARCHY_UNIQUE_NAME",
                            "ELEMENT_CLASS":"XMLAHierarchy",
                            "XMLA_FUNC":"getMDSchemaHierarchies",
                            "RESTRICT_ON":["DIMENSION"]},
    "CATALOG_HIERARCHY": {"RESTRICTION_NAME":"HIERARCHY_UNIQUE_NAME",
                          "PROPERTY_NAME":"HIERARCHY_UNIQUE_NAME",
                          "ELEMENT_CLASS":"XMLAHierarchy",
                          "XMLA_FUNC":"getMDSchemaHierarchies",
                          "RESTRICT_ON":[]},
    "DIMENSION": {"RESTRICTION_NAME":"DIMENSION_UNIQUE_NAME",
                  "PROPERTY_NAME":"DIMENSION_UNIQUE_NAME",
                  "ELEMENT_CLASS":"XMLADimension",
                  "XMLA_FUNC":"getMDSchemaDimensions",
                  "RESTRICT_ON":["CUBE"]},
    "CATALOG_DIMENSION": {"RESTRICTION_NAME":"DIMENSION_UNIQUE_NAME",
                          "PROPERTY_NAME":"DIMENSION_UNIQUE_NAME",
                          "ELEMENT_CLASS":"XMLADimension",
                          "XMLA_FUNC":"getMDSchemaDimensions",
                          "RESTRICT_ON":[]},
    "MEASURE": {"RESTRICTION_NAME":"MEASURE_UNIQUE_NAME",
                "PROPERTY_NAME":"MEASURE_UNIQUE_NAME",
                "ELEMENT_CLASS":"XMLAMeasure",
                "XMLA_FUNC":"getMDSchemaMeasures",
                "RESTRICT_ON":["CUBE"]},
    "CATALOG_MEASURE": {"RESTRICTION_NAME":"MEASURE_UNIQUE_NAME",
                        "PROPERTY_NAME":"MEASURE_UNIQUE_NAME",
                        "ELEMENT_CLASS":"XMLAMeasure",
                        "XMLA_FUNC":"getMDSchemaMeasures",
                        "RESTRICT_ON":[]},
    "SET": {"RESTRICTION_NAME":"SET_NAME",
            "PROPERTY_NAME":"SET_NAME",
            "ELEMENT_CLASS":"XMLASet",
            "XMLA_FUNC":"getMDSchemaSets",
            "RESTRICT_ON":["CUBE"]},
    "CATALOG_SET": {"RESTRICTION_NAME":"SET_NAME",
                    "PROPERTY_NAME":"SET_NAME",
                    "ELEMENT_CLASS":"XMLASet",
                    "XMLA_FUNC":"getMDSchemaSets",
                    "RESTRICT_ON":[]},
    "LEVEL": {"RESTRICTION_NAME":"LEVEL_UNIQUE_NAME",
              "PROPERTY_NAME":"LEVEL_UNIQUE_NAME",
              "ELEMENT_CLASS":"XMLALevel",
              "XMLA_FUNC":"getMDSchemaLevels",
              "RESTRICT_ON":["CUBE", "HIERARCHY"]},
    "MEMBER": {"RESTRICTION_NAME":"MEMBER_UNIQUE_NAME",
               "PROPERTY_NAME":"MEMBER_UNIQUE_NAME",
               "ELEMENT_CLASS":"XMLAMember",
               "XMLA_FUNC":"getMDSchemaMembers",
               "RESTRICT_ON":["CUBE", "HIERARCHY", "LEVEL"]},
    "HIERARCHY_MEMBER": {"RESTRICTION_NAME":"MEMBER_UNIQUE_NAME",
                         "PROPERTY_NAME":"MEMBER_UNIQUE_NAME",
                         "ELEMENT_CLASS":"XMLAMember",
                         "XMLA_FUNC":"getMDSchemaMembers",
                         "RESTRICT_ON":["CUBE", "HIERARCHY"]},
    "DIMENSION_MEMBER": {"RESTRICTION_NAME":"MEMBER_UNIQUE_NAME",
                         "PROPERTY_NAME":"MEMBER_UNIQUE_NAME",
                         "ELEMENT_CLASS":"XMLAMember",
                         "XMLA_FUNC":"getMDSchemaMembers",
                         "RESTRICT_ON":["DIMENSION"]},
    "CUBE_DIMENSION_MEMBER": {"RESTRICTION_NAME":"MEMBER_UNIQUE_NAME",
                              "PROPERTY_NAME":"MEMBER_UNIQUE_NAME",
                              "ELEMENT_CLASS":"XMLAMember",
                              "XMLA_FUNC":"getMDSchemaMembers",
                              "RESTRICT_ON":["CUBE", "DIMENSION"]},
    "TREE_MEMBER": {"RESTRICTION_NAME":"MEMBER_UNIQUE_NAME",
                    "PROPERTY_NAME":"MEMBER_UNIQUE_NAME",
                    "ELEMENT_CLASS":"XMLAMember",
                    "XMLA_FUNC":"getMDSchemaMembers",
                    "RESTRICT_ON":["CUBE", "HIERARCHY"]},
    "PROPERTY": {"RESTRICTION_NAME":"PROPERTY_NAME",
                 "PROPERTY_NAME":"PROPERTY_NAME",
                 "ELEMENT_CLASS":"XMLAProperty",
                 "XMLA_FUNC":"getMDSchemaProperties",
                 "RESTRICT_ON":["CUBE", "HIERARCHY", "LEVEL"]}

    }

