from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyRouteDelete(Service):
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
        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-route-delete'].conn

        # payload
        name = data.name + "blah"
        payload = {"name":name} }
        response = conn.delete(self.cid, payload)
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

outconn:holo-proxy-route-delete:
    http://localhost:8001
    /routes/
    Kong proxy

"""