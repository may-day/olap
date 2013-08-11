"""
This is an attempt to solve the concurrency problem that arise when two or more connections
are about to be authenticated via kerberos.

A first implementation of requests_kerberos held the kerberos context as an instance variable of HTTPKerberosAuth.
This fails when two connections are authenticated concurrently.
So the idea is to attach the kerberos context to the connection itself.
The problem is that the connection that is in need to be authenticated is already released back into the connection pool by the time
the HTTPKerberosAuth.handle_401 method is run. This is because the HTTPAdapter.send method reads the data (if not in stream mode).

So how can i make sure i get the very connection back from the pool when i send my authentication code?

My solution:
Upon each call to session.send i create my own HTTP adapter.
This adapter holds a reference to the original adapter.
When a connection is requested the first time i defer to the original adapter and then ask the returned pool manager for a connection.
This connection i put in the pool controled by my own adapter.
Thus the original adapter's pool has one less connection available and my pool has exactly one connection.
This connection is reused throughout the session.send call.
A hook is added to release the connection back into the original pool.

"""
import requests.adapters
import logging

log = logging.getLogger(__name__)

class FixedConnectionAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, pooledAdapter):
        super(FixedConnectionAdapter, self).__init__(pool_connections=1, pool_maxsize=1)
        self.pooledAdapter = pooledAdapter
        self.wraped_conn_pool = None
        self.timeout = None
        self.pool = None
        self.real_conn = None
        self.krb5_context = None
        # we catch exceptions in session.send and will call this hook
        self.call_on_exception = True

    def build_response(self, req, resp):
        req.register_hook("response", self)
        r=super(FixedConnectionAdapter, self).build_response(req, resp)
        return r

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        self.timeout = timeout
        return super(FixedConnectionAdapter, self).send(request, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)

    def get_connection(self, url, proxies=None):
        if self.pool is None:
            self.wraped_conn_pool=self.pooledAdapter.get_connection(url, proxies)
            if hasattr(self.wraped_conn_pool, 'proxy_pool'):
                self.wraped_conn_pool = self.wraped_conn_pool.proxy_pool
            
            self.pool = super(FixedConnectionAdapter, self).get_connection(url, proxies)
            if hasattr(self.pool, 'proxy_pool'):
                self.pool = self.pool.proxy_pool

            # initially, the queue is filled with None entries, so remove one to be able  putting a real one in
            try:
                self.pool.pool.get_nowait()
            except: pass

            # now instead of requesting/making new connections in our pool
            # we request a connection from the wrapped pool and put it into out own
            self.real_conn = self.wraped_conn_pool._get_conn(self.timeout)
            log.debug("borrowed connection: %s", self.real_conn)
            self.pool._put_conn(self.real_conn)
        return self.pool

    def __call__(self, r, **kwargs):
        if not (self.pool is None):
            log.debug("release_conn %s into original pool", self.real_conn)
            self.wraped_conn_pool._put_conn(self.real_conn)
            self.pool = None
        return r
