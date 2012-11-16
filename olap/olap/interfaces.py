'''
Created on 18.04.2012

@author: norman
'''
#@PydevCodeAnalysisIgnore

from zope.interface import Interface

class ConnectionException(Exception): pass
class OlapException(Exception):
    def __init__(self, message, detail):
            super(OlapException, self).__init__(message)
            self.detail = detail
            
class IProvider(Interface):
    """
    This covers all provider specifics.
    """
    
    def connect(**connectparams):
        """
        Connect to OLAP Server and return an IConnection instance or
        throws an exception.
        What parameters are needed is left to the actual olap provider. 
        """
        
    
class IConnection(Interface):
    """
    Talk to the backend through this.
    """

    def getOLAPSource():
        """Return an IOLAPSource providing object."""

class IOLAPSchemaElement(Interface):
    def getElementProperties():
        """Return a dictionary of this element's properties."""

class IOLAPSource(Interface):

    def getCatalogs():
        """Returns a list of ICatalogs in the Datasource."""

    def getCatalog(unique_name):
        """Returns a ICatalog in the Datasource with the given unique name."""

class ICatalog(IOLAPSchemaElement):
    def getCubes():
        """Returns a list of ICube in the catalog."""

    def getCube(unique_name):
        """Returns a ICube in the catalog with the given unique name."""

    def getDimensions(unique_name=None):
        """Returns a list of IDimension in the catalog optionally 
        matching the given name."""

    def getDimension(unique_name):
        """Returns a IDimension in the Catalog with the given unique name."""

    def getHierarchies(unique_name=None):
        """Returns a list of IHierarchy in the catalog optionally 
        matching the given name."""

    def getHierarchy(unique_name):
        """Returns a IHierarchy in the catalog with the given unique name."""

    def getSets(unique_name=None):
        """Returns a list of ISet in the catalog optionally 
        matching the given name."""

    def getSet(unique_name):
        """Returns a ISet in the catalog with the given unique name."""

    def getMeasures(unique_name=None):
        """Returns a list of IMeasure in the catalog optionally 
        matching the given name."""

    def getMeasure(unique_name):
        """Returns a IMeasure in the catalog with the given unique name."""

    def query(mdx_stmt):
        """Return a IMDXResult resulting from executing the mdx statement."""

class IMDXResult(Interface):
    def getSlice(properties=None, **kw):
        """
        getSlice(properties=None [,Axis<Number>=n|Axis<Number>=[i1,i2,..,ix]])
        
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
    def getAxisTuple(axis):
        """Returns the tuple on axis with name <axis>, usually 'Axis0', 'Axis1', 'SlicerAxis'.
        If axis is a number return tuples on the <axis>-th axis."""


class ICube(IOLAPSchemaElement):

    def getHierarchies():
        """Returns a list of IHierarchy related to the cube."""

    def getHierarchy(unique_name):
        """Returns a IHierarchy in the cube with the given unique name."""

    def getMeasures():
        """Returns a list of IMeasure in this cube."""

    def getMeasure(unique_name):
        """Returns a IMeasure in the cube with the given unique name."""

    def getSets():
        """Returns a list of ISet in this cube."""

    def getSet(unique_name):
        """Returns a ISet with the given unique name in the cube."""

    def getDimensions():
        """Returns a list of IDimension in the cube"""

    def getDimension(unique_name):
        """Returns a IDimension in the cube with the given unique name."""

class IDimension(IOLAPSchemaElement):

    def getHierarchies():
        """Returns a list of IHierarchy related to the cube."""

    def getHierarchy(unique_name):
        """Returns a IHierarchy in the cube with the given unique name."""

    def getMembers():
        """Returns a list of IMember in the dimension."""

    def getMember(unique_name):
        """Returns a IMember of the given name in the dimension."""

class IHierarchy(IOLAPSchemaElement):

    def getLevels():
        """Returns a list of ILevel in the hierarchy."""

    def getLevel(unique_name):
        """Returns a ILevel in the hierarchy with the given unique name."""

    def getMembers():
        """Returns a list of IMember in the hierarchy."""

    def getMember(unique_name):
        """Returns a IMember of the given name in the hierarchy."""

class ILevel(IOLAPSchemaElement):

    def getMembers():
        """Returns a list of IMember from this level."""

    def getProperties():
        """Returns a list of IProperty in the level."""

    def getProperty(unique_name):
        """Returns a IProperty with the given unique name in the level."""

class IMember(IOLAPSchemaElement):

    def getParent():
        """Return this member's parent member unique or None if this is the root
        already."""

    def getChildren():
        """Return this member's children in a list."""

    def hasChildren():
        """Returns True if this mmeber has children False otherwise."""

    def getSiblings():
        """Return this member's siblings in a list."""

    def hasSiblings():
        """Returns True if this mmeber has siblings False otherwise."""

    def getAncestors():
        """Return the member's line of ancestors in a list (self not included)."""

class IMeasure(IOLAPSchemaElement):
    pass

class IProperty(IOLAPSchemaElement):
    pass

class ISet(IOLAPSchemaElement):
    pass
