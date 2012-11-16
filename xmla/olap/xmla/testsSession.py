'''
Created on 16.06.2012

@author: norman

SSAS Tests are done against the Adventure Works DW 2008R2, tested against ssas version 10.50.2500.0 (comes with sqlserver 2008 R2)
Mondrian was test with version 3.3.0.14703

@author: norman

n.b.:
  Mondrian is running with a mysql backend. 
  Using the distributed embedded derby backend fails in MDSchemaMembers with an internal error (when
  a subselect is executed in the read-only container where the database lives).
  
'''

import unittest
import olap.xmla.xmla as xmla



mondrian={
"type":"mondrian",
"spn":None,          
"location":"http://localhost:8080/mondrian/xmla",
"username":None,
"password":None,
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
}

ssas={
"type":"ssas",
"spn":"HOST@DWH-BI",
"location":"http://dwh-bi/olap/msmdpump.dll",
"username":None,
"password":None,
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
"schema_tables":1
}

iccube={
"type":"icCube",
"spn":"",
"location":"http://localhost:80/icCube/xmla",
"username":"demo",
"password":"demo",
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
}

supported = None
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


class TestXMLA(unittest.TestCase):
    
    def setUp(self):
        self.be = mondrian
        self.p = xmla.XMLAProvider()
        self.c = self.p.connect(location=self.be["location"], username=self.be["username"], password=self.be["password"], spn=self.be["spn"])

    def testSessionBegin(self):
        self.c.BeginSession()
        self.c.EndSession()
        #print self.c.getDatasources()

        
def test_suite():
    #import s4u2p
    #s4u2p.authGSSKeytab("/home/norman/workspace/olap/host.keytab")
    return unittest.makeSuite(TestXMLA)

