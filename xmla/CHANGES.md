CHANGES
=======

0.7.2
-----
* now relies on requests 1.2.3
* fixed race condition in kerberos auth

0.7.1
-----
* kerberos-auth was sent twice

0.7
---
* works now with requests 0.14- and 1.-series of requests
* selection of cell properties failed

0.6
----
* dependency on kerberos and s4u2p is now optional
* added optional kerberos-sspi package for kerberos on windows through sspi via pywin32

0.5
----
* ``as_user`` and ``spn`` are no longer ignored in the kerberos authentication
* implemented the procedural interface from olap.interfaces
* fixed problem when no sliceraxis info is returned
* parameter ``property`` of getSlice now spells ``properties``

0.4
----
* keyword ``kerberos`` is gone. kerberos auth need is detected automatically
* ``BeginSession`` and ``EndSession`` provide XMLA Sessionsupport
* changes to work with icCube XMLA provider

0.3
----
* changed keyword ``doKerberos`` in XMLProvider.connect to ``kerberos``
* added ``sslverify`` keyword to XMLProvider.connect defaulting to ``True``.
  This will be handed to requests get method, so you can point it to your certificate bundle file.


0.2
----
* removed dependencies on specific versions in setup.py