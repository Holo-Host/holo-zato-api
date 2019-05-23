from zato.server.service import Service
from json import dumps
from anyjson import loads
from bunch import bunchify
import httplib
"""

"""

class HoloInitFdId(Service):
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
        if self.checkKey(data, 'contact_id') == True:
            params = {'contact_id': data.contact_id}
            conn = self.outgoing.plain_http['freshdesk-contact-id'].conn

            # Invoke the resource providing all the information on input
            request = dumps({'description': data.public_key})
            response = conn.put(self.cid, request, params=params)

            # response = {"hey":"ho"}
            # self.logger.info(response.json())
            self.logger.info(response.json())
            data = bunchify(loads(response.text))
            #response = Bunch()
            #self.response.payload = dumps(data.tags)
            # if "closedAlpha" not in data.tags:
            #     self.response.status_code = httplib.OK
            #     no_tag = {"result": "You must Contact Customer Support to participate in closed alpha. Please visit https://help.holo.host"}
            #     self.response.payload = dumps(no_tag)
            # else:
            #     tag_found = {"result":"AUTHORIZED for closed alpha" }
            #     self.response.payload = dumps(tag_found)
            self.response.payload =dumps(data)

        else:
            response = {"error": "request must contain contact_id"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)


"""
This service requires `contact_id` and `public_key`
public_key is derived from the holoport hc public key
contact_id is the freshdesk id

uses the following server objects

outconn:freshdesk-contact-id:
    https://holo.freshdesk.com
    /api/v2/contacts/{contact_id}
    application/json
    HTTP Basic Auth
    freshdesk	

rest-channel:holo-init-register
    	/holo-init-update
    	 holo-fd-id.holo-init-fd-id 
    	apikey (a generic one I create that all rest channels can use)


"""