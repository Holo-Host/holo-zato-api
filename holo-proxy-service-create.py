from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyServiceCreate(Service):
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
            response = {"error": "request must contain a service name"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'protocol'):
            response = {"error": "request must contain a protocol"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'host'):
            response = {"error": "request must contain a host"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'port'):
            response = {"error": "request must contain a port"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return

        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-service-create'].conn

        # Invoke the resource providing all the information on input
        # -- for testing. this GET returns all services
        # response = conn.get(self.cid)
        # -- for real
        # payload is name, protocol, host, port
        # {"name":"pubkey.holohost.net", "protocol":"https", "host":"1.2.3.4", "port":48080}
        name = data.name
        protocol = data.protocol
        host = data.host
        port = data.port
        payload = {"name":name, "protocol":protocol, "host":host, "port":port}
        response = conn.post(self.cid, payload)
        # if no response
        """
        if not response:
            response = {"error": "no response"}
            self.response.status_code = httplib.BAD_GATEWAY # 502
            self.response.payload = dumps(response)
            return
            """
        # else
        self.response.payload = dumps(response.json())
        return

"""

uses the following server objects

outconn:holo-proxy-service-create:
    http://localhost:8001
    /services/
    Kong proxy

"""