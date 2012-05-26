'''
Created on 20.05.2012

@author: norman
'''
import suds.transport.https
import suds.transport.http
from urllib2_kerberos import HTTPKerberosAuthHandler


class KerberosHttpAuthenticated(suds.transport.https.HttpAuthenticated):
    """
    Provides Kerberos http authentication.
    """
        
    def __init__(self, as_user=None, spn=None):
        self.as_user = as_user
        self.spn = spn
        suds.transport.https.HttpAuthenticated.__init__(self)
        
    def u2handlers(self):
        handlers = suds.transport.http.HttpTransport.u2handlers(self)
        handlers.append(HTTPKerberosAuthHandler(self.as_user, self.spn))
        return handlers