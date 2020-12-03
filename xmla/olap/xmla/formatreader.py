from .utils import *
import types
from olap.interfaces import IMDXResult
import zope.interface
from collections import namedtuple
from zeep import ns

nsmap = {
    "soap": ns.SOAP_11,
    "soap-env": ns.SOAP_ENV_11,
    "wsdl": ns.WSDL,
    "xsd": ns.XSD,
    "sql": "urn:schemas-microsoft-com:xml-sql"
}


@zope.interface.implementer(IMDXResult)
class TupleFormatReader(object):

    def __init__(self, tupleresult):
        self.root = tupleresult
        self.cellmap = self.mapOrdinalsToCells()

    def mapOrdinalsToCells(self):
        "Return a dict mapping ordinals to cells"
        m = {}
        # "getattr" for the case where there are no cells
        # aslist if there is only one cell
        if self.root.get("CellData"):
            for cell in aslist(getattr(self.root.CellData, "Cell", [])):
                m[int(cell._CellOrdinal)] = cell

        return m

    def getCellByOrdinal(self, ordinal):
        return self.cellmap.get(ordinal, {})

    def getAxisTuple(self, axis):
        """Returns the tuple on axis with name <axis>, usually 'Axis0', 'Axis1', 'SlicerAxis'.
        If axis is a number return tuples on the <axis>-th axis.
        If no axis information are available the return None.
        """
        res = None
        try:
            if isinstance(axis, stringtypes):
                ax = [x for x in aslist(self.root.Axes.Axis) if x._name == axis][0]
            else:
                ax = aslist(self.root.Axes.Axis)[axis]
            res = []
            for tup in aslist(getattr(ax.Tuples, "Tuple", [])):
                res.append(tup.Member)
        except AttributeError:
            pass
        return res

    def getSlice(self, properties=None, **kw):
        """
        getSlice(property=None [,Axis<Number>=n|Axis<Number>=[i1,i2,..,ix]])
        
        Return the resulting cells from a MDX statement. 
        The result is presented as an array of arrays of arrays of... 
        depending on amount of axes in the MDX.
        You can carve out slices you need by listing the indices of the axes
        you are interested in.

        Examples:
        
        result.getSlice() # return all
        result.getSlice(Axis0=3) # carve out the 4th column
        result.getSlice(Axis0=3, SlicerAxis=0) # same as above, SlicerAxis is ignored
        result.getSlice(Axis1=[1,2]) # return the data sliced at the 2nd and 3rd row
        result.getSlice(Axis0=3, Axis1=[1,2]) # return the data sliced at the 2nd and 
                                                3rd row in addition to the 4th column
        
        If you do not want the whole cell returned but just a single property of it 
        (like the Value) name that property in the property parameter:
        
        # from all the cells just get me the Value property
        result.getSlice(properties="Value") 
        # from all the cells just get me the Value property
        result.getSlice(properties=["Value", "FmtValue"]) 
        
        """
        axisranges = []  # list per axis the element indices to include

        # n.b: this assumes, axis are listed from Axis0,...AxisN in the ExecuteResponse,
        # otherwise the ordinal values would be useless anyway

        # at this offset we find the first requested index of the dimension
        firstindexoffset = 2
        hyperelemcount = 1

        axlist = aslist(getattr(self.root.Axes, "Axis", []))
        # filter out possible SlicerAxis
        axlist = [ax for ax in axlist if ax._name != "SlicerAxis"]

        for ax in axlist:

            if ax._name in kw:
                # only include listed indices
                indexrange = kw[ax._name]
                if isinstance(indexrange, int):
                    indexrange = [indexrange]

                # are the tupleindices valid?
                maxtups = len(getattr(ax.Tuples, "Tuple", []))
                toolarge = [idx for idx in indexrange if idx >= maxtups or idx < 0]
                if toolarge:
                    raise ValueError(
                        "The tuple requested do not exist on axis '%s': %s" % \
                        (ax._name, indexrange))

            else:
                # include all possible indices
                indexrange = list(range(len(getattr(ax.Tuples, "Tuple", []))))

            if not indexrange:
                # we have requested an empty set from an axis
                # by calling sth like this: getSlice(Axis2=[])
                # this renders the whole result empty
                # it could also because there was an empty set on an axis 
                # (i.e. "select {} on columns, [measure].members on rows from [some cube]")
                # anyway, we can simply stop here an return []

                # @@@WHY: shouldn't we rather return a result which dimensionality 
                # is one less than the amount of axes suggest?
                # or more generally:
                #      (#Axes - #EmptyAxes) == dim(result) (not counting SlicerAxis)
                return []

            # first element is a helper to calc the ordinal value from a cell's coord, 
            # second is the iteration index
            indexrange = [hyperelemcount * x for x in indexrange]
            axisrange = [firstindexoffset, []] + indexrange
            axisranges.append(axisrange)
            # hyperelemcount for the n-th Axis is the number
            # of cells in the subcube spanned by Axis(0)..Axis(n-1)
            hyperelemcount = hyperelemcount * len(ax.Tuples.Tuple)

        # add an entry for the slicer
        axisranges.append([firstindexoffset, [], 0])

        lastdimchange = 0
        while lastdimchange < len(axisranges):
            # calc ordinal number of cell
            ordinal = 0
            for axisrange in axisranges:
                hyperelemcount = axisrange[axisrange[0]]
                ordinal = ordinal + hyperelemcount

            cell = self.getCellByOrdinal(ordinal)
            if properties is None:
                axisranges[0][1].append(cell)
            else:
                if isinstance(properties, stringtypes):
                    d = getattr(cell, properties,
                                None)
                else:
                    d = {}
                    for prop in aslist(properties):
                        d[prop] = getattr(cell, prop,
                                          None)
                axisranges[0][1].append(d)

            # advance to next requested element in slice
            lastdimchange = 0
            while lastdimchange < len(axisranges):
                axisrange = axisranges[lastdimchange]
                if axisrange[0] < len(axisrange) - 1:
                    axisrange[0] = axisrange[0] + 1
                    break
                else:
                    axisrange[0] = firstindexoffset

                lastdimchange = lastdimchange + 1
                if lastdimchange < len(axisranges):
                    axisranges[lastdimchange][1].append(axisrange[1])
                    axisrange[1] = []

        # as the last dimension is the sliceraxis it has only one member, 
        # so we can safely unpack the first element
        # in that element our resulting multidimensional array has been accumulated
        return axisranges[lastdimchange - 1][1][0]


@zope.interface.implementer(IMDXResult)
class DAXFormatReader(object):

    def __init__(self, root_raw, root):
        self.root = root
        self.root_raw = root_raw
        self.res_raw = getattr(root, "row", [])
        if self.res_raw:
            self.res = aslist(self.res_raw)
        self.rows = []
        self.description = self._get_description()
        self._arrangeData()

    def _get_description(self):
        """
        Return description from a single row.

        We only return the name, type (inferred from the data) and if the values
        can be NULL. String columns in Druid are NULLable. Numeric columns are NOT
        NULL.
        """
        ret = []
        res = self.root_raw.findall("xsd:schema/xsd:complexType[@name='row']/xsd:sequence/xsd:element",
                                    namespaces=nsmap)

        for i in range(len(res)):
            c = res[i]

            t = c.attrib.get('type')
            ret.append(
                {
                    "name": c.attrib.get("{{{}}}field".format(nsmap["sql"])),
                    "type": t
                }
            )
        return ret

    def _arrangeData(self):
        Row = None
        for irow in range(len(self.res)):
            row = self.res[irow]

            if Row is None:
                keys = [d["name"] for d in self.description]
                Row = namedtuple('Row', keys, rename=True)

            values = []

            for key, value in row.items():
                if key != "text":
                    values.append(value)
            self.rows.append(Row(*values))

