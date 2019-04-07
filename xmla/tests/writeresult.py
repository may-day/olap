#! /usr/bin/env python
import olap.xmla.xmla as xmla
import olap.xmla.utils as utils
import pprint
import os.path
from requests_kerberos import HTTPKerberosAuth
from requests.auth import HTTPBasicAuth
from zeep import Plugin

class LogRequest(Plugin):
    def __init__(self):
        self.res=""

    def ingress(self, envelope, http_headers, operation):
        self.res=utils.etree_tostring(envelope)

def main(mdxfile, location, catalog, krb, username, password, spn, sslverify):
    p = os.path.dirname(os.path.realpath(__file__))
    pyfile = os.path.join(p, os.path.splitext(mdxfile)[0] + os.path.extsep + "py")
    cmd = open(os.path.join(p,mdxfile)).read()

    p = xmla.XMLAProvider()

    auth = None
    if krb:
        kw = {}
        if spn:
            service, host = spn.split("@",1)
            kw["service"]=service
            kw["hostname_override"]=host
        if username:
            kw["principal"] = username
        auth = HTTPKerberosAuth(**kw)
    elif username:
        auth = HTTPBasicAuth(username, password)
    
    kwargs = {}
    log = LogRequest()
    kwargs["log"] = log
    c=p.connect(location=location, sslverify=sslverify, auth=auth, **kwargs)
    res=c.Execute(cmd, Catalog=catalog)
    x=utils.dictify(res.root, keep_none_text=True)

    erg=pprint.pformat(x)
    encodinghint="# -*- coding: utf-8"
    open(pyfile, "w+").write('%s\n"""\n%s\n"""\n\nresult=%s\n\nxml_response="""%s"""' % (encodinghint, cmd, erg, log.res))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MDX Resultwriter.")
    parser.add_argument("mdxfile")
    parser.add_argument("--location", dest="location", 
                        help="location von XMLASource", 
                        default="http://localhost:8080/xmondrian/xmla")
    parser.add_argument("--catalog", dest="catalog", 
                        help="catalog to execute the mdx in", 
                        default="FoodMart")
    parser.add_argument("--username", dest="username", help="connect as user", 
                        default=None)
    parser.add_argument("--password", dest="password", help="use password", 
                        default=None)
    parser.add_argument("--krb", action="store_const", const=True, default=False, dest="krb", 
                        help="kerberos auth")
    parser.add_argument("--spn", dest="spn", 
                        help="spn, defaults to HTTP@host if omitted")
    parser.add_argument("--sslverify", dest="sslverify", default=True,
                        help="sslverify, either False or path of cert file")
    args = parser.parse_args()

    if isinstance(args.sslverify, str):
        if args.sslverify.upper() in ["0", "FALSE", "NO", "NEIN"]:
            args.sslverify = False

    main(args.mdxfile, args.location, args.catalog, args.krb,
         args.username, args.password, args.spn, args.sslverify)

