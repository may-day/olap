olap.xmla
=========

This package is meant for accessing xmla datasources - see
http://en.wikipedia.org/wiki/XML\_for\_Analysis

Builing
=======

In this directory, run:

::

    python setup.py build

Testing
=======

Tests are done against the Mondrian, SSAS, icCube XMLA providers. The
testsDiscover module tests behavior with different XMLA providers with
the Discover command while testsExecute does the same with the Execute
command. Note that you likely need to modify the sources if you want to
test yourself since they contain specifics (namely the location of the
services and names of the data sources).

Sample
======

Here is an example how to use it:

.. code:: python

    import olap.xmla.xmla as xmla

    p = xmla.XMLAProvider()
    # mondrian
    c = p.connect(location="http://localhost:8080/mondrian/xmla")
    # to analysis services (if iis proxies requests at /olap/msmdpump.dll)
    # you will need a valid kerberos principal of course
    # c = p.connect(location="https://my-as-server/olap/msmdpump.dll", 
    #               sslverify="/path/to/my/as-servers-ca-cert.pem")
    # to icCube
    # c = p.connect(location="http://localhost:8282/icCube/xmla", username="demo", 
    #               password="demo")

    # getting info about provided data
    print(c.getDatasources())
    print(c.getMDSchemaCubes())
    # for ssas a catalog is needed, so the call would be like
    # get a catalogname from a call to c.getDBSchemaCatalogs()
    # c.getMDSchemaCubes(properties={"Catalog":"a catalogname"})

    # execute a MDX (working against the foodmart sample catalog of mondrian)
    cmd= """select {[Measures].ALLMEMBERS} * {[Time].[1997].[Q2].children} on columns, 
    [Gender].[Gender].ALLMEMBERS on rows 
    from [Sales]
    """

    res = c.Execute(cmd, Catalog="FoodMart")
    #return only the Value property from the cells
    res.getSlice(properties="Value")
    # or two props
    res.getSlice(properties=["Value", "FmtValue"]) 

    # to return some subcube from the result you can
    # return all
    res.getSlice()
    # carve out the 4th column
    res.getSlice(Axis0=3) 
    # same as above, SlicerAxis is ignored
    res.getSlice(Axis0=3, SlicerAxis=0) 
    # return the data sliced at the 2nd and 3rd row
    res.getSlice(Axis1=[1,2]) 
    # return the data sliced at the 2nd and 3rd row and at the 4th column
    res.getSlice(Axis0=3, Axis1=[1,2]) 

Using the procedural interface:

.. code:: python

    import olap.xmla.xmla as xmla

    p = xmla.XMLAProvider()
    c = p.connect(location="http://localhost:8080/mondrian/xmla")
    s = c.getOLAPSource()

    # import olap.interfaces as oi
    # oi.IOLAPSource.providedBy(s) == True

    s.getCatalogs()
    s.getCatalog("FoodMart").getCubes()
    s.getCatalog("FoodMart").getCube("HR").getDimensions()
    s.getCatalog("FoodMart").getCube("HR").getDimension("[Department]").\
    getMembers()
    s.getCatalog("FoodMart").getCube("HR").getDimension("[Department]").\
    getMember("[Department].[14]")

    cmd= """select {[Measures].ALLMEMBERS} * {[Time].[1997].[Q2].children} on columns, 
    [Gender].[Gender].ALLMEMBERS on rows 
    from [Sales]
    """
    res=s.getCatalog("FoodMart").query(cmd)
    res.getSlice()

Note
----

The contained vs.wsdl originates from the following package:
http://www.microsoft.com/en-us/download/confirmation.aspx?id=9388 and
was subsequently modified (which parameters go in the soap header) to
work with the suds package.olap.xmla

