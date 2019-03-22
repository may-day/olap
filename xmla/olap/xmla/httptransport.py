"""
Implementation of Transport based on the requests package.
This packages lets us reuse connections. 
"""

from suds.transport import Transport, Reply, TransportError
from suds.properties import Unskin
from six.moves.http_cookiejar import CookieJar
from logging import getLogger
import requests as req
from .requests_kerberosauth import HTTPKerberosAuth
import six.moves.urllib.request as url
import sys
from . import sessions

log = getLogger(__name__)


class DummyFile:
    def __init__(self, content):
        self.data = content
    def read(self):
        return self.data
    def close(self):
        pass

# on windows urlopen doesn't work with file:// if it contains a drive specification
if sys.platform.startswith("win"):
    from six.moves.urllib.response import addinfourl
    import os
    import email.utils
    import email
    import mimetypes

    class MyDriveFileHandler(url.FileHandler):
        def open_local_file(self, req):
            try:
                host = req.host
                filename = req.selector
                # if that bombs, then go on with original method
                localfile = url.url2pathname(host+filename)
                stats = os.stat(localfile) 
                size = stats.st_size
                modified = email.utils.formatdate(stats.st_mtime, usegmt=True)
                mtype = mimetypes.guess_type(filename)[0]
                headers = email.message_from_string(
                        'Content-type: %s\nContent-length: %d\nLast-modified: %s\n' %
                        (mtype or 'text/plain', size, modified))
                origurl = 'file://' + host + filename
                return addinfourl(open(localfile, 'rb'), headers, origurl)
            except:
                pass
            return url.FileHandler.open_local_file(self, req)

class HttpTransport(Transport):
    """
    HTTP transport using urllib2.  Provided basic http transport
    that provides for cookies, proxies but no authentication.
    """
    
    def __init__(self, **kwargs):
        """
        @param kwargs: Keyword arguments.
            - B{proxy} - An http proxy to be specified on requests.
                 The proxy is defined as {protocol:proxy,}
                    - type: I{dict}
                    - default: {}
            - B{timeout} - Set the url open timeout (seconds).
                    - type: I{float}
                    - default: 90
        """
        Transport.__init__(self)
        self.sslverify = kwargs.pop("sslverify")
        Unskin(self.options).update(kwargs)
        self.cookiejar = CookieJar()
        self.proxy = {}
        self.urlopener = None
        self.session = sessions.Session()
        self.session.proxies = self.proxy
        self.session.verify=self.sslverify
         
    def open(self, request):
        log.debug('opening (%s)', request.url)
        self.proxy = self.options.proxy
        res = self.doOpen(request.url)
        # TODO: fake a file like object if it isn't already
        if isinstance(res, req.models.Response):
            res = DummyFile(res.content)
        return res

    def send(self, request):
        msg = request.message
        headers = request.headers
        self.proxy = self.options.proxy
        log.debug('sending:\n%s', request)
        resp = self.doOpen(request.url, data=msg, headers=headers, cookies=self.cookiejar)
        if resp.status_code not in (200,):
            raise TransportError("Error: %s"%resp.reason, resp.status_code, DummyFile(resp.content))
        result = Reply(resp.status_code, resp.headers, resp.content)
        log.debug('received:\n%s', result)
        #except u2.HTTPError, e:
        #    if e.code in (202,204):
        #        result = None
        #    else:
        #        raise TransportError(e.msg, e.code, e.fp)
        return result

    def doOpen(self, theUrl, data=None, headers=None, cookies=None, **moreargs):
        """
        Open a connection.
        @param theUrl: an url
        @type theUrl: string
        @return: The opened file-like object or requests Response object.
        @rtype: fp or requests.models.Response
        """
        # d'oh, requests doesn't know what to do with a file schema... 
        # so fall back to good old trusted urllib2
        if theUrl.startswith("file://"):
            if sys.platform.startswith("win") and theUrl[8:9] == ":":
                # we likely have a drive letter, which urlopen will fail with :(
                try:
                    return url.build_opener(MyDriveFileHandler).open(theUrl)
                except:
                    raise
            return url.urlopen(theUrl)
        tm = self.options.timeout
        self.modifyargs(moreargs)
        return self.session.request("GET" if data is None else "POST", 
                                    theUrl, data=data, headers=headers, 
                                    cookies=cookies, timeout=tm, **moreargs)
            
    def __deepcopy__(self, memo={}):
        clone = self.__class__()
        p = Unskin(self.options)
        cp = Unskin(clone.options)
        cp.update(p)
        return clone

    def modifyargs(self, moreargs):
        pass


class HttpAuthenticated(HttpTransport):
    """
    Provides basic http authentication for servers that don't follow
    the specified challenge / response model.  This implementation
    appends the I{Authorization} http header with base64 encoded
    credentials on every http request.
    """
    
    def modifyargs(self, moreargs):
        HttpTransport.modifyargs(self, moreargs)
        if self.credentials()[0] is not None:
            moreargs["auth"] = self.credentials()
        
    def credentials(self):
        return (self.options.username, self.options.password)
    
class HttpKerberosAuthenticated(HttpTransport):
    """
    Provides basic http authentication for servers that don't follow
    the specified challenge / response model.  This implementation
    appends the I{Authorization} http header with base64 encoded
    credentials on every http request.
    """
    
    def __init__(self, as_user=None, spn=None, **kwargs):
        HttpTransport.__init__(self, **kwargs)
        self.as_user = as_user
        self.spn = spn
        self.auth = HTTPKerberosAuth(as_user=as_user, spn=spn, 
                                     sslverify=self.sslverify, proxies=self.proxy)
        
    def modifyargs(self, moreargs):
        HttpTransport.modifyargs(self, moreargs)
        moreargs["auth"] = self.auth

