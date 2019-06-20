from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyServiceRead(Service):
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
        if not self.checkKey(data, 'service_id'):
            response = {"error": "request must contain a service_id"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-service-read'].conn

        # params
        service_id = data.service_id
        params = {"service_id":service_id}

        # Invoke the resource providing all the information on input
        try:
            response = conn.get(self.cid, params)
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

outconn:holo-proxy-service-read:
    http://localhost:8001
    /services/
    Kong proxy

"""