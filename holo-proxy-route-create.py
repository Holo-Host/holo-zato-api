from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyRouteCreate(Service):
    def checkKey(self, d, key):
        return key in d

    def handle(self):
        # miscellaneous logging
        self.logger.info(self.request.raw_request)
        self.logger.info('cid:[{}]'.format(self.cid))
        # prep data
        data = self.request.bunchified()
        self.logger.info(data)
        # exit if missing incoming data
        if not self.checkKey(data, 'name'):
            response = {"error": "request must contain a route name"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'protocols'):
            response = {"error": "request must contain protocols array"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'hosts'):
            response = {"error": "request must contain hosts array"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'service'):
            response = {"error": "request must contain a service"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return

        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-route-create'].conn

        # Invoke the resource providing all the information on input
        # -- for testing. this GET returns all routes
        # response = conn.get(self.cid)
        # -- for real
        # payload is name, protocols, hosts, service id
        # {"name":"pubkey.holohost.net","protocols":["http","https"], "hosts":["pubkey.holohost.net"], "service":"e311425e-3f56-4e70-84c7-fb1790a60316"}
        name = data.name
        protocols = data.protocols
        hosts = data.hosts
        service = data.service
        payload = {"name":name, "protocols":protocols, "hosts":hosts, "service":{"id":service} }
        response = conn.post(self.cid, payload)
        # if no response
        """
        if not response:
            response = {"error": "no response"}
            self.response.status_code = httplib.BAD_GATEWAY
            self.response.payload = dumps(response)
            return
            """
        # else
        self.response.payload = dumps(response.json())
        return

"""

uses the following server objects

outconn:holo-proxy-route-create:
    http://localhost:8001
    /routes/
    Kong proxy

"""