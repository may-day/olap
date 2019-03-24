import unittest
from olap.xmla.formatreader import TupleFormatReader
import olap.xmla.utils as utils
from . import mdx1
from . import mdx_noaxistuple
from . import mdx_columns_but_no_rows
from . import mdx_rows_but_no_columns_no_cells

"""
import olap.xmla.xmla as xmla
p = xmla.XMLAProvider()
c=p.connect(location="http://localhost:8080/xmondrian/xmla")
res=c.Execute(cmd, Catalog="FoodMart")
"""
class TestFormatReader(unittest.TestCase):

    longMessage=True
    maxDiff = 2000
    def setUp(self):
        self.res = utils.PropDict(mdx1.result)
        self.fr=TupleFormatReader(self.res)
        self.cm = self.fr.cellmap
        self.ordinal1 = list(filter(lambda cell: cell._CellOrdinal == "1", self.res.CellData.Cell))[0]
        self.ax_tupel0 = [tup.Member for tup in self.res.Axes.Axis[0].Tuples.Tuple]

        self.res_noaxistuple = utils.PropDict(mdx_noaxistuple.result)
        self.fr_noaxistuple=TupleFormatReader(self.res_noaxistuple)

        res=utils.PropDict(mdx_columns_but_no_rows.result)
        self.fr_cbnr=TupleFormatReader(res)

        res=utils.PropDict(mdx_rows_but_no_columns_no_cells.result)
        self.fr_rbncnc=TupleFormatReader(res)

    def testOrdinalsToCells(self):
        self.assertIsInstance(self.cm, dict)

        # should be the same
        self.assertEqual(self.ordinal1, self.cm[1])

    def testGetCellByOrdinal(self):
        self.assertEqual(self.ordinal1, self.fr.getCellByOrdinal(1))
        self.assertEqual({}, self.fr.getCellByOrdinal(-1))

    def testGetAxisTuple(self):
        self.assertEqual(self.ax_tupel0, self.fr.getAxisTuple(0))
        self.assertEqual(self.ax_tupel0, self.fr.getAxisTuple("Axis0"))
        self.assertRaises(IndexError, self.fr.getAxisTuple, *[7])
        self.assertRaises(IndexError, self.fr.getAxisTuple, *["Axis7"])
        
        # if there are no axis information
        self.assertEqual(None, self.fr_noaxistuple.getAxisTuple("Axis0"))

        # some actually return empty tuples,
        # e.g. "select {} on columns, [Gender].[Gender].ALLMEMBERS on rows from [Sales]"
        # which would have no tuples on Axis1
        # we mock that here

        del self.res.Axes.Axis[0].Tuples.Tuple
        self.assertEqual([], self.fr.getAxisTuple(0))

    def testGetSlice_without_SlicerAxis(self):
        c = {}
        fr = self.fr
        cm = fr.cellmap
        for (k,v) in cm.items(): c[k] = v.Value

        cube =[
            [c[0], c[1], c[2], c[3]],
            [c[4], c[5], c[6], c[7]]
            ]

        self.assertEqual(cube, fr.getSlice(properties="Value"), "whole")
        self.assertEqual(cube, fr.getSlice(properties="Value", SlicerAxis=1),
                          "whole, ignore SlicerAxis kw")

        cube =[
            [c[0], c[2], c[3]],
            [c[4], c[6], c[7]]
            ]

        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[0,2,3]),
                          "come tuples from axis0, others fully")

        cube =[
            [c[0], c[2], c[3]]
            ]

        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[0,2,3], Axis1=0),
                          "some tuples from all axes")

        self.assertEqual([], fr.getSlice(properties="Value", Axis0=[]), "dropping axis")

        # requesting non-existing tuples from an axis
        self.assertRaises(ValueError, fr.getSlice, **{"Axis0":[7]})

        # getting the whole cell
        cube =[
            [cm[0]] # cm instead of c
            ]

        self.assertEqual(cube, fr.getSlice(Axis0=0, Axis1=0), "whole cell")

        # getting more than one property cell
        cube =[[
                {"Value":cm[0]["Value"],
                 "FmtValue":cm[0]["FmtValue"]
                 }
                ]]
        self.assertEqual(cube, fr.getSlice(properties=["Value", "FmtValue"], 
                                            Axis0=0, Axis1=0), "few properties")

        # changing order
        cube =[
            [c[3], c[2], c[1]]
            ]

        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[3,2,1], Axis1=0), 
                          "changing order")

    def testGetSlice_no_axes_1_cell(self):
        """ case: select from [Sales] """
        c = {}
        fr = self.fr_noaxistuple
        cm = fr.cellmap
        for (k,v) in cm.items(): c[k] = v.Value

        cube =c[0]

        self.assertEqual(cube, fr.getSlice(properties="Value"), "whole")
        self.assertEqual(cube, fr.getSlice(properties="Value", SlicerAxis=1), "whole1")
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=0), "1st col")
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis1=0), "1st row")
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[]), "no cols")

    def testGetSlice_columns_but_no_rows(self):
        """ case: select [Measures].AllMembers on columns from [Sales] """
        c = {}
        fr = self.fr_cbnr
        cm = fr.cellmap
        for (k,v) in cm.items(): c[k] = v.Value

        cube =[c[0], c[1]]

        self.assertEqual(cube, fr.getSlice(properties="Value"), "whole")
        self.assertEqual(cube, fr.getSlice(properties="Value", SlicerAxis=1), "whole1")
        cube =[c[0]]
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=0), "1st col")
        cube =[c[0], c[1]]
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis1=0), "1st row")
        cube =[]
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[]), "no cols")
        self.assertRaises(ValueError, fr.getSlice, **{"Axis0":[7]})

    def testGetSlice_columns_but_no_rows_and_no_cells(self):
        """
        works on SSAS:
        select {} on columns, [some hierarchy].ALLMEMBERS from [somecube]
        """
        c = {}
        fr = self.fr_rbncnc
        cm = fr.cellmap
        for (k,v) in cm.items(): c[k] = v.Value

        cube =[]

        self.assertEqual(cube, fr.getSlice(properties="Value"), "whole")
        self.assertEqual(cube, fr.getSlice(properties="Value", SlicerAxis=1), "whole1")
        self.assertEqual(cube, fr.getSlice(properties="Value", Axis0=[]), "no cols")


