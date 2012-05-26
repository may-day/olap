'''
Created on 18.04.2012

@author: norman
'''
#@PydevCodeAnalysisIgnore

from zope.interface import Interface
import zope.schema
from olap import xmla

class XMLAProperty(zope.schema.Text):
    "Extends Text with an attribute saying whether the property can be used to restrict a search."
     
    def __init__(self, restriction=False, **kw):
        super(XMLAProperty, self).__init__(**kw)
        self.restriction = restriction

class XMLAContainer(zope.schema.Container):
    "Container with an attribute saying whether it can be used to restrict a search."
     
    def __init__(self, restriction=False, **kw):
        super(XMLAContainer, self).__init__(**kw)
        self.restriction = restriction
        
class IXMLADataSource(Interface):
    """
    """
    dataSourceName = XMLAProperty(title=u"DataSourceName", 
                                  description=u"The name of the data source.",
                                  required=True,
                                  restriction=True
                                 )
    dataSourceDescription = XMLAProperty(title=u"DataSourceDescription", 
                                  description=u"Text describing the data source.",
                                  required=False,
                                  restriction=False
                                 )
    url = XMLAProperty(title=u"URL",
                       description=u"URL to this data source.",
                       required=False,
                       restriction=True)
    dataSourceInfo = XMLAProperty(title=u"DataSourceInfo",
                                  description=u"Additional information that is required to connect to the data source.",
                                  required=False,
                                  restriction=False)
    providerName = XMLAProperty(title=u"ProviderName",
                                description=u"Name of this data sources provider.",
                                required=False,
                                restriction=True)
    providerType = XMLAContainer(title=u"ProviderType",
                                 description=u"Types of data supported.",
                                 required=True,
                                 restriction=True)
    authenticationMode= XMLAProperty(title=u"AuthenticationMode",
                                     description=u"What kind of authentication is supported by this data source.",
                                     required=True,
                                     restriction=True)
    
        
    
class IConnection(Interface):
    """
    Talk to the backend through this.
    """
    
    def getDataSources():
        """
        Return a list of IXMLADataSource.
        """ 
        