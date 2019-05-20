from zato.server.service import Service
from json import dumps
import httplib


class HoloInitEmail(Service):
    def checkKey(self, dict, key):
        if key in dict:
            return True
        else:
            return False

    def handle(self):
        self.logger.info(type(self.request.raw_request))
        self.logger.info(self.request.raw_request)
        self.logger.info('cid:[{}]'.format(self.cid))
        # params = {'network_id': 'e5cd7a9e1c3e8c42', 'member_id': 'e294a96f8c'}
        # headers = {'Authorization': 'bearer gjd1vJCHJkfLheKkoRTihepuTXW9FRwV'}
        data = self.request.bunchified()
        if self.checkKey(data, 'email') == True:
            params = {'email': data.email}
            conn = self.outgoing.plain_http['freshdesk-email-lookup'].conn

            # Invoke the resource providing all the information on input
            response = conn.get(self.cid, params)

            # response = {"hey":"ho"}
            # self.logger.info(response.json())
            self.logger.info(type(response.json()))
            if not response.json():
                self.response.status_code = httplib.NOT_FOUND
                empty_response = {"email": data.email, "status": "NOT FOUND"}
                self.response.payload = dumps(empty_response)
            else:
                self.response.payload = dumps(response.json())

        else:
            response = {"error": "request must contain email address"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)


"""

uses the following server objects

outconn:freshdesk-email-lookup:
    https://holo.freshdesk.com
    /api/v2/contacts?email={email}	
    HTTP Basic Auth
    freshdesk	

rest-channel:holo-init-email
    	/holo-init-email
    	holo-init-email.holo-init-email
    	apikey (a generic one I create that all rest channels can use)


"""