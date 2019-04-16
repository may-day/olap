'''
Created on 18.04.2012
- For SSAS tests are done against the Adventure Works DW 2008R2.
- For Mondrian tests are done against the FoodMart sample data source.

@author: norman

n.b.:
  Mondrian is running with a mysql backend. 
  Using the distributed embedded derby backend fails in MDSchemaMembers with an internal error (when
  a subselect is executed in the read-only container where the database lives).
  
'''

import unittest
import olap.xmla.xmla as xmla
from nose.tools import *
from requests.auth import HTTPBasicAuth
import tests.integration.execute_mondrian as execute_mondrian
import tests.integration.execute_ssas as execute_ssas
import tests.mockhelper as mockhelper

mock_location = "mock://somewhere/over/the/rainbow"

mondrian={
    "type":"mondrian",
    "location":"http://localhost:8080/xmondrian/xmla",
    "auth": None,
    "catalog":"FoodMart",
    "cube":"[Sales]",
    "set1":"[Measures].ALLMEMBERS",
    "set2":"[Time].[1997].[Q2].children",
    "set3":"[Gender].[Gender].ALLMEMBERS",
    "conversation":execute_mondrian,
}
ssas={
	"type":"ssas",
	"location":"http://dwh-bi/olap/msmdpump.dll",
    "auth" : None,
	"catalog":"Adventure Works DW 2008R2",
	"cube":"[Sales Summary]",
	"set1":"[Measures].ALLMEMBERS",
	"set2":"[Date].[Month of Year].ALLMEMBERS",
	"set3":"[Product].[Product Categories].[Category].ALLMEMBERS",
    "conversation":execute_ssas,
}

class XMLAExecute(object):
    be = None
    logreq = None
    record = False

    def setUp(self):
        testname = self.id().split(".")[-1]
        session = mockhelper.mockedsession(self.be["conversation"], testname)

        self.cube = self.be["cube"]
        self.set1 = self.be["set1"]
        self.set2 = self.be["set2"]
        self.set3 = self.be["set3"] 
        self.catalog = self.be["catalog"]
        self.p = xmla.XMLAProvider()
        if self.logreq:
            self.logreq.prefix=testname
        kw = {
            "log":self.logreq,
            "session":session
        }
        self.c = self.p.connect(location=self.be["location"], auth=self.be["auth"], **kw)
        
    def tearDown(self):
        if self.logreq and self.record:
            self.logreq.saveConversation(fname="try_execute_"+self.be["type"] +".py")

    def test2Axes(self):
        cmd= """select {%(set1)s} * {%(set2)s} on columns, 
                       %(set3)s on rows 
                from %(cube)s""" %\
	    {"set1":self.set1, "set2":self.set2, "set3":self.set3, 
	     "cube":self.cube}

        erg = self.c.Execute(cmd, Catalog=self.catalog)
        erg.getSlice(property="Value")

    def test3Axes(self):
        cmd= """select %(set1)s on columns, 
                       %(set2)s on rows, %(set3)s on Axis(2) 
                from %(cube)s""" %\
	    {"set1":self.set1, "set2":self.set2, "set3":self.set3, 
	     "cube":self.cube}
        erg = self.c.Execute(cmd, Catalog=self.catalog)
        erg.getSlice(property="Value")

    def testNoAxesButOneCell(self): 
    # well there is a sliceraxis of course ...
        cmd= "select from %(cube)s" % {"cube":self.cube}
        erg = self.c.Execute(cmd, Catalog=self.catalog)
        erg.getSlice(property="Value")

    def testOneDimensional(self): 
	# columns with cells but no rows
        cmd= "select %(set1)s on columns from %(cube)s" %\
	    {"cube":self.cube, "set1":self.set1}
        erg = self.c.Execute(cmd, Catalog=self.catalog)
        erg.getSlice(property="Value")

    def testOneDimensional2(self): 
        # empty column with no cells but rows
        if self.be["type"] == "mondrian": return # NPE in Mondrian's backend
        cmd= "select {} on columns, %(set1)s on rows from %(cube)s" %\
	    {"cube":self.cube, "set1":self.set1}
        erg = self.c.Execute(cmd, Catalog=self.catalog)
        erg.getSlice(property="Value")
		

try:
    from testconfig import config
    server=config['xmla']['server'] or ""
    server = server.split(",")
    for server_section in server:
        if server_section in globals():
            globals()[server_section].update(config.get(server_section, {}))

    do_record=(config['xmla']['record'] or "no") == "yes"

    if "ssas" in server:
        from requests_kerberos import HTTPKerberosAuth
        ssas["auth"] = HTTPKerberosAuth()

except:
    # we mock responses
    server=["mondrian", "ssas"]
    config = {}
    mondrian["location"]=mock_location
    ssas["location"]=mock_location
    do_record = False

if "mondrian" in server:
    class TestMondrian(XMLAExecute, unittest.TestCase):
        be = mondrian
        logreq = mockhelper.LogRequest(False)
        record = do_record

if "ssas" in server:
    class TestSSAS(XMLAExecute, unittest.TestCase):
        be = ssas
        logreq = mockhelper.LogRequest(False)
        record = do_record
        

