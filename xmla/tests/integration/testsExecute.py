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

mondrian={"type":"mondrian",
	  "location":"http://localhost:8080/mondrian/xmla",
	  "username":None,
	  "password":None,
	  "spn":"dummy",
	  "catalog":"FoodMart",
	  "cube":"[Sales]",
	  "set1":"[Measures].ALLMEMBERS",
	  "set2":"[Time].[1997].[Q2].children",
	  "set3":"[Gender].[Gender].ALLMEMBERS",
}
ssas={
	"type":"ssas",
	"location":"http://dwh-bi/olap/msmdpump.dll",
	"username":None,
	"password":None,
	"spn":"HOST@DWH-BI",
	"catalog":"Adventure Works DW 2008R2",
	"cube":"[Sales Summary]",
	"set1":"[Measures].ALLMEMBERS",
	"set2":"[Date].[Month of Year].ALLMEMBERS",
	"set3":"[Product].[Product Categories].[Category].ALLMEMBERS",
}

iccube={
	"type":"icCube",
	"spn":"",
	"location":"http://localhost:80/icCube/xmla",
	"username":"demo",
	"password":"demo",
	"catalog":"Sales",
	"cube":"[Sales]",
	"set1":"[Measures].ALLMEMBERS",
	"set2":"[Time].[Month].ALLMEMBERS",
	"set3":"[Product].[Product].[Category].ALLMEMBERS",
	}


class XMLAExecute(object):
    be = None

    def setUp(self):
        self.cube = self.be["cube"]
	self.set1 = self.be["set1"]
	self.set2 = self.be["set2"]
	self.set3 = self.be["set3"] 
	self.catalog = self.be["catalog"]
        self.p = xmla.XMLAProvider()
	self.c = self.p.connect(location=self.be["location"], 
				username=self.be["username"], 
				password=self.be["password"], 
				spn=self.be["spn"])

    def tearDown(self):
        pass

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
            
except:
    server=[]
    config = {}

if "mondrian" in server:
    class TestMondrian(XMLAExecute, unittest.TestCase):
        be = mondrian

if "iccube" in server:
    class TestICCube(XMLAExecute, unittest.TestCase):
        be = iccube

if "ssas" in server:
    class TestSSAS(XMLAExecute, unittest.TestCase):
        be = ssas

