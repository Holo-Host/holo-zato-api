from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyRouteList(Service):
    def handle(self):
        # miscellaneous logging
        self.logger.info(self.request.raw_request)
        self.logger.info('cid:[{}]'.format(self.cid))
        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-route-list'].conn

        # Invoke the resource providing all the information on input
        try:
            response = conn.get(self.cid)
        except:
            response = {"error": "something broke"}
            self.response.status_code = httplib.BAD_GATEWAY # 502
            self.response.payload = dumps(response)
            return
        else:
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

outconn:holo-proxy-route-list:
    http://localhost:8001
    /routes/
    Kong proxy

"""