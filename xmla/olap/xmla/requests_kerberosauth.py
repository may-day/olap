'''
Created on 22.05.2012

@author: norman
'''
from requests.auth import AuthBase
from requests.compat import urlparse
from requests import get as reqget
from requests import session
import kerberos as k
import s4u2p
import re
import logging

def getLogger():
    log = logging.getLogger("http_kerberos_auth_handler")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

log = getLogger()

class HTTPKerberosAuth(AuthBase):
    """Attaches Kerberos Authentication to the given Request object."""
    
    rx = re.compile('(?:.*,)*\s*Negotiate\s*([^,]*),?', re.I)
    auth_header = 'www-authenticate'

    def __init__(self, as_user=None, spn=None, gssflags=k.GSS_C_MUTUAL_FLAG|k.GSS_C_SEQUENCE_FLAG):
        self.retried = 0
        self.context = None
        self.gssflags=gssflags
        self.spn = spn
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
    
    def handle_401(self, r):
        """Takes the given response and tries kerberos negotiation, if needed."""

        ret = r
        r.request.deregister_hook('response', self.handle_401)

        neg_value = self.negotiate_value(r.headers) #Check for auth_header
        firstround = False
        if neg_value is not None:
            
            if self.context is None:
                spn = self.get_spn(r)
                result, self.context = self.gss_init(spn, self.gssflags)
                
                if result < 1:
                    log.warning("gss_init returned result %d" % result)
                    return None

                firstround = False
                log.debug("gss_init() succeeded")

            result = self.gss_step(self.context, neg_value)

            if result < 0:
                self.gss_clean(self.context)
                self.context = None
                log.warning("gss_step returned result %d" % result)
                return None

            log.debug("gss_step() succeeded")

            if result == k.AUTH_GSS_CONTINUE or (result == k.AUTH_GSS_COMPLETE and not (self.gssflags & k.GSS_C_MUTUAL_FLAG) and firstround):
                response = self.gss_response(self.context)
                r.request.headers['Authorization'] = "Negotiate %s" % response
                r.request.send(anyway=True)
                _r = r.request.response
                _r.history.append(r)

                ret = _r
            if result == k.AUTH_GSS_COMPLETE and self.context:
                 self.gss_clean(self.context)
                 self.context = None

        return ret

    def __call__(self, r):
        r.register_hook('response', self.handle_401)
        return r

def test(args):
    log.setLevel(logging.DEBUG)
    log.info("starting test")
    if args.keytab:
        s4u2p.authGSSKeytab(args.keytab)
    s = session(auth=HTTPKerberosAuth(as_user=args.user, spn=args.spn))
    r=s.get(args.url)
    print r.text
#    if website is set up to keep auth, the next calls will not authenticate again
#    (in IIS accomplish this by setting the windowsAuthentication properties: authPersistNonNTLM="true" and authPersistSingleRequest="false")
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
