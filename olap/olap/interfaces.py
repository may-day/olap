'''
Created on 18.04.2012

@author: norman
'''
#@PydevCodeAnalysisIgnore

from zope.interface import Interface

class ConnectionException(Exception): pass

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
    
        