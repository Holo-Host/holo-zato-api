from zato.server.service import Service
from json import dumps
import httplib

class HoloProxyServiceDelete(Service):
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
        # else

        # Obtains a connection object
        conn = self.outgoing.plain_http['holo-proxy-service-delete'].conn

        # payload
        name = data.name
        payload = {"service_name":name}

        # Invoke the resource providing all the information on input
        try:
            response = conn.delete(self.cid, payload)
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
            # Kong's reesponse to DELETE is a 204 No Content always
            # therefore we can't return anything at this time
            # self.response.payload = dumps(response.json())
            return

"""

uses the following server objects

outconn:holo-proxy-service-delete:
    http://localhost:8001
    /services/
    Kong proxy

"""
