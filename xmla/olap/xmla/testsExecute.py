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
be = mondrian
cube, set1, set2, set3, catalog = be["cube"], be["set1"], be["set2"], be["set3"], be["catalog"]

class TestXMLAExecute(unittest.TestCase):
	def setUp(self):
		self.p = xmla.XMLAProvider()
		self.c = self.p.connect(location=be["location"], username=be["username"], password=be["password"], spn=be["spn"])

	def tearDown(self):
		pass

	def test2Axes(self):
		cmd= "select {%(set1)s} * {%(set2)s} on columns, %(set3)s on rows from %(cube)s" % {"set1":set1, "set2":set2, "set3":set3, "cube":cube}

		erg = self.c.Execute(cmd, Catalog=catalog)
		erg.getSlice(property="Value")

	def test3Axes(self):
		cmd= "select %(set1)s on columns, %(set2)s on rows, %(set3)s on Axis(2) from %(cube)s" % {"set1":set1, "set2":set2, "set3":set3, "cube":cube}
		erg = self.c.Execute(cmd, Catalog=catalog)
		erg.getSlice(property="Value")

	def testNoAxesButOneCell(self): # well there is a sliceraxis of course ...
		cmd= "select from %(cube)s" % {"cube":cube}
		erg = self.c.Execute(cmd, Catalog=catalog)
		erg.getSlice(property="Value")

	def testOneDimensional(self): # columns with cells but no rows
		cmd= "select %(set1)s on columns from %(cube)s" % {"cube":cube, "set1":set1}
		erg = self.c.Execute(cmd, Catalog=catalog)
		erg.getSlice(property="Value")

	def testOneDimensional2(self): # empty column with no cells but rows
		if be["type"] == "mondrian": return # NPE in Mondrian's backend
		cmd= "select {} on columns, %(set1)s on rows from %(cube)s" % {"cube":cube, "set1":set1}
		erg = self.c.Execute(cmd, Catalog=catalog)
		erg.getSlice(property="Value")
		

def test_suite():
	return unittest.makeSuite(TestXMLAExecute)

