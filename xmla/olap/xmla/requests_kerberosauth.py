'''
Created on 22.05.2012

@author: norman
'''
from requests.auth import AuthBase
from requests.compat import urlparse
from requests import __version__ as reqver
import re
import logging
import os.path
import time

log = logging.getLogger(__name__)

# this will still let you talk to other non kerberos protected sites
# and the calling http module can proceed

try:
    import kerberos as k
except:
    try:
        import kerberos_sspi as k
    except:
        log.warning("No kerberos module, so you won't be able to talk to kerberos protected sites")
        def notimplemented_kerb(*args, **kw):
            raise Exception("failed to load kerberos")
        class k:
            authGSSClientStep = notimplemented_kerb
            authGSSClientResponse = notimplemented_kerb
            authGSSClientClean = notimplemented_kerb
            authGSSClientInit = notimplemented_kerb
            GSSError = notimplemented_kerb
            GSS_C_MUTUAL_FLAG = 0
            GSS_C_SEQUENCE_FLAG = 0
try:
    import s4u2p
except:
    log.warning("No s4u2p module, so you won't be able to impersonate a user.")
    def notimplemented_s4u2p(*args, **kw):
        raise Exception("failed to load s4u2p")
    class s4u2p:
        authGSSClientStep = notimplemented_s4u2p
        authGSSClientResponse = notimplemented_s4u2p
        authGSSClientClean = notimplemented_s4u2p
        authGSSClientInit = notimplemented_s4u2p
        GSSError = notimplemented_s4u2p
        GSS_C_MUTUAL_FLAG = 0
        GSS_C_SEQUENCE_FLAG = 0

class HTTPKerberosAuth(AuthBase):
    """Attaches Kerberos Authentication to the given Request object."""
    
    rx = re.compile('(?:.*,)*\s*Negotiate\s*([^,]*),?', re.I)
    auth_header = 'www-authenticate'

    def __init__(self, as_user=None, spn=None, gssflags=k.GSS_C_MUTUAL_FLAG|k.GSS_C_SEQUENCE_FLAG
                 , sslverify=True, proxies=None):
        self.sslverify = sslverify
        self.proxies   = proxies
        self.retried   = 0
        self.gssflags  = gssflags
        self.spn       = spn
        if as_user:
            self.gss_step = s4u2p.authGSSImpersonationStep
            self.gss_response = s4u2p.authGSSImpersonationResponse
            self.gss_clean = s4u2p.authGSSImpersonationClean
            self.gss_init = lambda *args: s4u2p.authGSSImpersonationInit(as_user, *args)
            self.GSSError = s4u2p.GSSError
        else:
            self.gss_step = k.authGSSClientStep
            self.gss_response = k.authGSSClientResponse
            self.gss_clean = k.authGSSClientClean
            self.gss_init = k.authGSSClientInit
            self.GSSError = k.GSSError

    def negotiate_value(self, headers):
        """checks for "Negotiate" in proper auth header
        """
        authreq = headers.get(self.auth_header, None)

        if authreq:
            log.debug("authreq: %s", authreq)
            mo = self.rx.search(authreq)
            if mo:
                return mo.group(1)
            else:
                log.debug("regex failed on: %s" % authreq)

        else:
            log.debug("%s header not found" % self.auth_header)

        return None
    
    def get_spn(self, r):
        if self.spn is None:
            domain = urlparse(r.url).hostname
            self.spn = spn = "HTTP@%s" % domain
            log.debug("calculated SPN as  %s" % spn)

        return self.spn

    def getContext(self, resp):
        return resp.connection.krb5_context

    def setContext(self, resp, context):
        resp.connection.krb5_context = context

    def handle_401_guarded(self, r, **kwargs):
        try:
            res = self.handle_401(r, **kwargs)
        except Exception as e:
            self.setContext(r, None)
            r.reason = str(e)
            return r

        return res

    def handle_401(self, r, **kwargs):
        """Takes the given response and tries kerberos negotiation, if needed."""

        log.info("kerberosauth: handle_401...")
        ret = r

        neg_value = self.negotiate_value(r.headers) #Check for auth_header
        firstround = False
        if neg_value is not None:
            
            log.info("kerberosauth: neg_value not none")
  
            context = self.getContext(r)
            if context is None:
                spn = self.get_spn(r)
                result, context = self.gss_init(spn, self.gssflags)
                if result < 1:
                    raise Excetion("gss_init returned result %d" % result)

                firstround = False
                log.info("gss_init() succeeded")

            result = self.gss_step(context, neg_value)

            if result < 0:
                self.gss_clean(context)
                self.setContext(r, None)
                raise Excetion("gss_step returned result %d" % result)

            log.info("gss_step() succeeded")

            if result == k.AUTH_GSS_CONTINUE or \
                    (result == k.AUTH_GSS_COMPLETE and \
                         not (self.gssflags & k.GSS_C_MUTUAL_FLAG) and firstround):
                response = self.gss_response(context)
                req=r.request
                req.headers['Authorization'] = "Negotiate %s" % response

                r.content
                self.setContext(r, context)
                r.raw.release_conn()

                log.info("REQUESTS version %s", reqver)
                kwargs.setdefault("verify", self.sslverify)
                kwargs.setdefault("proxies", self.proxies)

                r2 = r.connection.send(req, **kwargs)
                r2.history.append(r)
                ret = self.handle_401(r2)

            if result == k.AUTH_GSS_COMPLETE and context:
                log.info("auth complete, now cleaning context...")
                self.gss_clean(context)
                self.setContext(r, None)

        return ret

    def __call__(self, r):
        r.register_hook('response', self.handle_401_guarded)
        return r

def test(args):
    from requests import session
    log.setLevel(logging.DEBUG)
    log.info("starting test")
    if args.keytab:
        s4u2p.authGSSKeytab(args.keytab)
    s = session(auth=HTTPKerberosAuth(as_user=args.user, spn=args.spn))
    r=s.get(args.url)
    print(r.text)
#    if website is set up to keep auth, the next calls will not authenticate again
#    (in IIS accomplish this by setting the windowsAuthentication properties: 
#       authPersistNonNTLM="true" and authPersistSingleRequest="false")
#    for i in range(20):
#        r=s.get(args.url)
#        print i, r.text
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Kerberos authentication handler for the requests package.")
    parser.add_argument("--user", dest="user", help="user to impersonate, otherwise the current kerberos principal will be used", default=None)
    parser.add_argument("--url", dest="url", help="kerberos protected site")
    parser.add_argument("--spn", dest="spn", help="spn to use, if not given HTTP@domain will be used")
    parser.add_argument("--keytab", dest="keytab", help="path to keytab if you won't use system's default one (only needed for impersonation)", default=None)
    args = parser.parse_args()
    
    test(args)
