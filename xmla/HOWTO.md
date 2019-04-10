How do i run the integration tests?
===================================

Since olap providers are not always available, i mock the responses using requests_mock. 

```
nosetests -v -w tests/integration
```

To run the tests against real servers, i use the same tests with a diffenrent config:

```
nosetests -v -c integrationtests.cfg
```

If part of the config reading/setup in test_Discover.py or test_Execute.py fails, it will fall back to use mocking. That means, if you elected to test against ssas, you will need requests_kerberos installed. You can set the types to test in `integrationtests.cfg`.

In `integrationtests.cfg` exists a `record=yes|no` entry to record the requests and responses in files, i.e. in `try_discover_ssas.py` when recording the tests in test_Discover.py against a SSAS server. Renaming them by dropping the `try_` prefix will use the recorded data in a mocked test.

How does it work?
==================

testDiscover:
-------------

The software will send DISCOVER messages for (all?, no not all) XMLA1.1 rowsets.
For that it will need configuration paramaters like the url of the XMLA service
or the username and password to use.
Many olap systems come with a sample database, i.e. AdventureWorks for SSAS or
FoodMart for Mondrian.
The tests simply use those databases to run against.
Since every system comes with a different sample database the details like which
catalog or which cube to test against are also captured in the configuration
parameters.
The used parameters you find at the top of the module, for instance the mondrian
configuration looks like this:

```python
mondrian={
"type":"mondrian",
"spn":None,          
"location":"http://localhost:8080/mondrian/xmla",
"auth":None,
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
"schema_tables":1
}
```

At the end of the modules you find the creation of testcase classes based on those
dictionaries, e.g.:

```python
if "mondrian" in server:
    class TestMondrian(XMLA, unittest.TestCase):
        be = mondrian
```

testExecute
------------

Here Execute messages are sent against different servers.
The used MDX statements vary to capture different aspects of results
like existing or missing axis information.
Note: the actual checking of results here is rather non existent :)


How can i disable/enable testruns against specific servers?
===========================================================

You can use the `integrationtests.cfg` file for that.

In there you find:

```
[nosetests]
where=tests/integration
tc-file=integrationtests.cfg
logging-level=INFO

[xmla]
#server=mondrian,iccube,ssas
server=mondrian

# overwrite any settings to match your environment
# which there are you can see in tests/integration/testsDiscover.py

[iccube]
location=http://localhost:8765/icCube/xmla
```


In the `[xmla]` section you can list list the servers to test.


How can i modify the parameters, like login name?
=================================================

You can use the `integrationtests.cfg` file for that.

Simply add a section for the server and make a key=value 
entry in there. 
For example, my icCube server runs on a different port 
than programmed in tests. So i add the correct entry
to the cfg file:

```
[iccube]
location=http://localhost:8765/icCube/xmla
```


How can i add a new server?
===========================

Say i want to add palo server tests.
In testDiscovery and testExecute i add a new
configuration dictionary:

```python
palo={
"type":"palo",
"spn":None,          
"location":"http://localhost:4242/",
"auth":HTTPBasicAuth("admin","admin"),
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
"schema_tables":1
}
```

Also add a derived testcase:

```python
if "palo" in server:
    class TestPalo(XMLA, unittest.TestCase):
        be = mondrian
```

In `integrationtests.cfg` change the `server` entry in the
`[xmla]` section to `palo`, like so:

```
[xmla]
#server=mondrian,iccube,ssas
server=palo
```

What are all those restrict_ values in the server config for?
=============================================================

These are the values of Restriction, Catalog, Properties etc. elements in an
XMLA message.
Most are reused in different tests. Some of the entries represent expected values
from the XMLA various requests. The naming of those keys is below optimal, you
would have to read the actual test method to gain insight to their meaning, sorry.