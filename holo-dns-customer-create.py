from zato.server.service import Service
from json import dumps
import httplib

class HoloDnsCustomerCreate(Service):
    def checkKey(self, d, key):
        return key in d

    def handle(self):
        # miscellaneous logging
        self.logger.info(type(self.request.raw_request))
        self.logger.info(self.request.raw_request)
        self.logger.info('cid:[{}]'.format(self.cid))
        # prep data
        data = self.request.bunchified()
        # exit if no pubkey incoming
        if not self.checkKey(data, 'type'):
            response = {"error": "request must contain a dns type"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'name'):
            response = {"error": "request must contain a dns name"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        if not self.checkKey(data, 'content'):
            response = {"error": "request must contain dns content"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return
        # else

        # kvdb
        service = 'zato.kvdb.data-dict.dictionary.get-value-list'

        ddrequest = {'system':'cloudflare', 'key': 'auth_key'}
        ddresponse = self.invoke(service, ddrequest)
        auth_key = ddresponse["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        self.logger.info(auth_key)

        ddrequest = {'system':'cloudflare', 'key': 'auth_email'}
        ddresponse = self.invoke(service, ddrequest)
        auth_email = ddresponse["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        self.logger.info(auth_email)

        # Headers the endpoint expects
        headers = {'X-Auth-Email':auth_email, 'X-Auth-Key':auth_key}

        ddrequest = {'system':'cloudflare', 'key': 'zone'}
        ddresponse = self.invoke(service, ddrequest)
        zone = ddresponse["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        self.logger.info(zone)

        # params
        params = {"zone":zone}

        # create payload
        # {"type":"CNAME", "name":"something", "content":"loader.holohost.net"}
        record_type = data.type
        name = data.name
        content = data.content
        payload = {"type":record_type, "name":name, "content":content}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-dns-customer-create'].conn

        # Invoke the resource providing all the information on input
        response = conn.post(self.cid, payload, params, headers=headers)
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

outconn:cloudflare-dns-customer-create:
    https://api.cloudflare.com
    /client/v4/zones/{zone}/dns_records
    Cloudflare API

"""