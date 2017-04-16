'''
Created on 22.05.2012

@author: norman
'''
import logging
import os.path

log = logging.getLogger(__name__)


def test(args):
    from olap.xmla import sessions, requests_kerberosauth
    log.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    log.addHandler(ch)

    log.info("starting test")
    if args.keytab:
        s4u2p.authGSSKeytab(args.keytab)
    s = sessions.Session()
    s.auth=requests_kerberosauth.HTTPKerberosAuth(as_user=args.user, spn=args.spn)
    r=s.get(args.url) #, auth=requests_kerberosauth.HTTPKerberosAuth(as_user=args.user, spn=args.spn))
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

