from zato.server.service import Service
from json import dumps
import httplib
import json

class HoloDnsDelete(Service):
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

        # ---------------- Part One -------------------- #
        # get domain id for domain

        # params
        domain = "*." + data.pubkey + ".holohost.net"
        dtype = "CNAME"
        params = {"zone":zone, "type":dtype, "domain":domain}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-dns-read'].conn

        # Invoke the resource providing all the information on input
        response = conn.get(self.cid, params, headers=headers)
        response_dict = response.json()
        domain_id = response_dict["result"][0]["id"]

        # ---------------- Part Two -------------------- #
        # DELETE domain by id

        # params
        params = {"zone":zone, "record_id":domain_id}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-dns-delete'].conn

        # Invoke the resource providing all the information on input
        response = conn.delete(self.cid, params, headers=headers)

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

outconn:cloudflare-dns-read:
    https://api.cloudflare.com
    /client/v4/zones/{zone}/dns_records
    Cloudflare API

outconn:cloudflare-dns-delete:
    https://api.cloudflare.com
    /client/v4/zones/{zone}/dns_records
    Cloudflare API

"""