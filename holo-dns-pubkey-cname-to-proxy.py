from zato.server.service import Service
from json import dumps
import httplib

class HoloDnsPubkeyCnameToProxy(Service):
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
        if not self.checkKey(data, 'pubkey'):
            response = {"error": "request must contain a public key"}
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
        # {"type":"CNAME", "name":"pubkey.holohost.net", "content":"proxy.holohost.net"}
        domain = "*." + data.pubkey + ".holohost.net"
        payload = {"type":"CNAME", "name":domain, "content":"proxy.holohost.net"}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-dns-create'].conn

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

outconn:cloudflare-dns-create:
    https://api.cloudflare.com
    /client/v4/zones/{zone}/dns_records
    Cloudflare API

"""