'''
Created on 18.04.2012

SSAS Tests are done against the Adventure Works DW 2008R2, 
tested against ssas version 10.50.2500.0 (comes with sqlserver 2008 R2)
Mondrian was test with version 3.3.0.14703

@author: norman

n.b.:
  Mondrian is running with a mysql backend. 
  Using the embedded derby backend (as distributed by mondrian) fails in 
  MDSchemaMembers with an internal error (when a subselect is executed in 
  the read-only container where the database lives).
  
'''

import unittest
from nose.tools import *
import olap.xmla.xmla as xmla
from requests_kerberos import HTTPKerberosAuth
from requests.auth import HTTPBasicAuth

from olap.xmla.connection import xmla1_1_rowsets

mondrian={
    "type":"mondrian",
    "auth": None,
    "location":"http://localhost:8080/xmondrian/xmla",
    "ds": "Provider=Mondrian;DataSource=MondrianFoodMart;",
    "catalog":"FoodMart",
    "restrict_cube":"HR",
    "restrict_dim":"Position",
    "restrict_unique_dim":"[Gender]",
    "cubes_expected":7,
    "restrict_funcname":"||",
    "restrict_hier":"Time",
    "restrict_level_unique_name":"[Employees].[Employee Id]",
    "restrict_hierarchy_unique_name":"[Time]",
    "cube_measures":5,
    "schema_levels":3,
    "schema_sets":1,
    "schema_sets_needs_cubename":False,
    "schema_tables":1
}

ssas={
    "type":"ssas",
    "location":"http://dwh-bi/olap/msmdpump.dll",
    "auth" : HTTPKerberosAuth(),
    "ds":"DWH-BI",
    "catalog":"Adventure Works DW 2008R2",
    "restrict_cube":"Adventure Works",
    "restrict_dim":"Account",
    "restrict_unique_dim":"[Account]",
    "cubes_expected":7,
    "restrict_funcname":"TRIM",
    "restrict_hier":"Account Number",
    "restrict_level_unique_name":"[Customer].[Customer Geography].[Country]",
    "restrict_hierarchy_unique_name":"[Customer].[Customer Geography]",
    "cube_measures": 51,
    "schema_levels":6,
    "schema_sets":1,
    "schema_sets_needs_cubename":True, # not really, but if you have a few DBs on your server this will bring it to it's knees
    "schema_tables":1
}

iccube={
    "type":"icCube",
    "location":"http://localhost:80/icCube/xmla",
    "auth": HTTPBasicAuth("demo", "demo"),
    "ds":"icCube-datasource",
    "catalog":"Sales",
    "restrict_cube":"Sales",
    "restrict_dim":"Customers",
    "restrict_unique_dim":"[Customers]",
    "cubes_expected":1,
    "restrict_funcname":"TRIM",
    "restrict_hier":"Geography",
    "restrict_level_unique_name":"[Customers].[Geography].[Region]",
    "restrict_hierarchy_unique_name":"[Customers].[Geography]",
    "cube_measures": 2,
    "schema_levels":4,
    "schema_sets":0,
    "schema_sets_needs_cubename":False,
    "schema_tables":0
}


import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


class XMLA(object):

    def setUp(self):
        self.p = xmla.XMLAProvider()
        self.c = self.p.connect(location=self.be["location"], 
                                auth=self.be["auth"])
        self.c.BeginSession()
        self.getSchemaRowsetSupport()
         
    def getSchemaRowsetSupport(self):
        if self.supported is None:
            self.supported=[x["SchemaName"] for x in self.c.getSchemaRowsets()]
            self.proprietary = [x for x in self.supported if not(x in xmla1_1_rowsets)]
            self.conform = [x for x in self.supported if (x in xmla1_1_rowsets)]
            self.unsupported = [x for x in xmla1_1_rowsets if not (x in self.supported)]
    
    def tearDown(self):
        self.c.EndSession()
        #pass
    
    def testGetDatasources(self):
        erg=self.c.getDatasources()
        assert_true(len(erg) == 1, "One Datasource is expected")
        assert_equal(self.be["ds"], erg[0]["DataSourceName"])
        
    def testGetProperties(self):
        erg=self.c.getProperties()
        # check fpr required xmla properties
        req = """AxisFormat,BeginRange,Catalog,Content,Cube,DataSourceInfo,
                 EndRange,Format,LocaleIdentifier,MDXSupport,Password,
                 ProviderName,ProviderVersion,StateSupport,Timeout,UserName"""
        # of those required icCube only returns ProviderVersion and Catalog
        if self.be == iccube: req = "Catalog,ProviderVersion"
        propnames = [x["PropertyName"] for x in erg]
        for p in req.split(","):
            assert_in(p.strip(), propnames)

    def testGetDBSchemaCatalogs(self):
        erg=self.c.getDBSchemaCatalogs()
        assert_true(len(erg) > 0, "One Catalog is expected - at least")
        assert_in(self.be["catalog"], [x["CATALOG_NAME"] for x in erg])
        
    
    def testGetDBSchemaColumns(self):
        if "DBSCHEMA_COLUMNS" in self.conform:
            erg=self.c.getDBSchemaColumns()
            assert_true(len(erg) > 0, 
                            "There must be at least one column, really!")
        
    def testGetDBSchemaTables(self):
        erg=self.c.getDBSchemaTables()
        assert_true(len(erg) >= self.be["schema_tables"], 
                        "There must be at least one table")

    def testGetDBSchemaProviderTypes(self):
        if "DBSCHEMA_PROVIDER_TYPES" in self.conform:
            erg=self.c.getDBSchemaProviderTypes()
            msg="There should be at least one type like INTEGER for example"
            assert_true(len(erg) > 0, msg)
        
    def testGetDBSchemaTablesInfo(self):
        if "DBSCHEMA_TABLES_INFO" in self.conform:
            erg=self.c.getDBSchemaTablesInfo()
            assert_true(len(erg) > 0, 
                            "There must be at least one tablesinfo")

    def testGetMDSchemaActions(self):
        erg=self.c.getMDSchemaActions(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], "COORDINATE":self.be["restrict_cube"], "COORDINATE_TYPE":1})
        assert_true(len(erg)==0, "no actions expected")

    def testGetMDSchemaCubes(self):
        # oh my, mondrian doesn't know what do do with Catalog in the Proplist ... 
        # but only when requesting cubes, other rowset requests are going 
        # through just fine (are probably ignored on the server side)
        props = {"Catalog":self.be["catalog"]}
        erg=self.c.getMDSchemaCubes(properties=props)
        assert_equals(len(erg), self.be["cubes_expected"])
        erg=self.c.getMDSchemaCubes(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties=props)
        assert_equals(len(erg), 1)

    def testGetSchemaRowsets(self):
        erg=self.c.getSchemaRowsets()
        assert_true(len(erg)>0, "at least one schema is expected")
        
    def testGetMDSchemaFunctions(self):
        erg=self.c.getMDSchemaFunctions()
        assert_true(len(erg)> 1, 
                        "There should be more than one function description.")
        erg=self.c.getMDSchemaFunctions(
            restrictions={"FUNCTION_NAME":self.be["restrict_funcname"]})
        assert_equals(len(erg), 1)
        
    def testGetMDSchemaMembers(self):
        erg=self.c.getMDSchemaMembers(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
                          "LEVEL_UNIQUE_NAME":self.be["restrict_level_unique_name"]}, 
            properties={"Catalog":self.be["catalog"]})
        assert_true(len(erg)> 1, 
                        "There should be more than one dimension member.")

    def testGetMDSchemaProperties(self):
        erg=self.c.getMDSchemaProperties(
            {"CUBE_NAME":self.be["restrict_cube"], 
             'LEVEL_UNIQUE_NAME': self.be["restrict_level_unique_name"]}, 
            properties={"Catalog":self.be["catalog"]})
        assert_true(len(erg)> 1, 
                        "There should be more than one schema property.")

    def testGetMDSchemaSets(self):
        if self.be["schema_sets_needs_cubename"]:
            erg=self.c.getMDSchemaSets(restrictions={"CUBE_NAME":self.be["restrict_cube"]})
        else:
            erg=self.c.getMDSchemaSets()
        
        assert_true(len(erg)>= self.be["schema_sets"], 
                        "There should be a schema set.")

    def testGetEnumerators(self):
        if "DISCOVER_ENUMERATORS" in self.conform:
            erg = self.c.getEnumerators()
            msg = "There should be at least one enumerator."
            assert_true(len(erg)> 0, msg)
        
    def testGetLiterals(self):
        erg = self.c.getLiterals()
        assert_true(len(erg)> 0, "There should be at least one literal.")
        
    def testGetKeywords(self):
        # instead of not listing the KEYWORDS Rowset in a call to 
        # DISCOVER_SCHEMA_ROWSETS, iccube throws an exceptions
        if "DISCOVER_KEYWORDS" in self.conform and self.be != iccube:
            erg = self.c.getKeywords()
            assert_true(len(erg)> 0, 
                            "There should be at least one keyword.")
        

    def testGetMDSchemaDimensions(self):
        erg=self.c.getMDSchemaDimensions(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
                          "DIMENSION_NAME":self.be["restrict_dim"]},
            properties={"Catalog":self.be["catalog"]})
        assert_equals(len(erg), 1)
        
    def testGetMDSchemaHierarchies(self):
        erg=self.c.getMDSchemaHierarchies(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        assert_true(len(erg)> 1, 
                        "There should be more than one hierarchy.")
        erg=self.c.getMDSchemaHierarchies(
            restrictions={"HIERARCHY_NAME":self.be["restrict_hier"], 
                          "CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        assert_equals(len(erg), 1)

    def testGetMDSchemaMeasures(self):
        erg=self.c.getMDSchemaMeasures(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        assert_equals(len(erg), self.be["cube_measures"])

    def testGetSchemaLevels(self):
        erg = self.c.getMDSchemaLevels(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
             'HIERARCHY_UNIQUE_NAME': self.be["restrict_hierarchy_unique_name"]},
            properties={"Catalog":self.be["catalog"]})
        assert_equals(len(erg), self.be["schema_levels"])
    
    def testGetDBSchemaSchemata(self):
        if "DBSCHEMA_SCHEMATA" in self.supported:
            erg = self.c.Discover("DBSCHEMA_SCHEMATA")


try:
    print("yo")
    from testconfig import config
    server=config['xmla']['server'] or ""
    server = server.split(",")
    for server_section in server:
        if server_section in globals():
            globals()[server_section].update(config.get(server_section, {}))
            
except:
    print("darn")
    server=[]
    config = {}

if "mondrian" in server:
    class TestMondrian(XMLA, unittest.TestCase):
        be = mondrian
        supported = proprietary = conform = unsupported = None

if "iccube" in server:
    class TestICCube(XMLA, unittest.TestCase):
        be = iccube
        supported = proprietary = conform = unsupported = None

if "ssas" in server:
    class TestSSAS(XMLA, unittest.TestCase):
        be = ssas
        supported = proprietary = conform = unsupported = None

#def test_suite():
#    #import s4u2p
#    #s4u2p.authGSSKeytab("/home/norman/workspace/olap/host.keytab")
#    return unittest.makeSuite(TestMondrian)

