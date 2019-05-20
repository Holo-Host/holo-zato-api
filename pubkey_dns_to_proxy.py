from zato.server.service import Service
from json import dumps
import httplib

class PubkeyDnsToProxy(Service):
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
        # create payload
        # {"type":"CNAME", "name":"pubkey.holohost.net", "content":"proxy.holohost.net"}
        domain = data.pubkey + ".holohost.net"
        payload = {"type":"CNAME", "name":domain, "content":"proxy.holohost.net"}

        # params
        params = {}

        # kvdb
        service = 'zato.kvdb.data-dict.dictionary.get-value-list'

        request = {'system':'cloudflare', 'key': 'auth_key'}
        response = self.invoke(service, request)
        auth_key = response["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        self.logger.info(auth_key)

        request = {'system':'cloudflare', 'key': 'auth_email'}
        response = self.invoke(service, request)
        auth_email = response["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        self.logger.info(auth_email)


        # Headers the endpoint expects
        headers = {'X-Auth-Email':auth_email, 'X-Auth-Key':auth_key}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-dns-create-entry'].conn

        # Invoke the resource providing all the information on input
        response = conn.post(self.cid, payload, params, headers=headers)

        self.response.payload = dumps(response.json())

        """
        #response = {"blah": "no errors, blah"}
        self.response.payload = dumps(response.json())
        """
        return

        """
        if not response.json():
            self.response.status_code = httplib.NOT_FOUND
            empty_response = {"email": data.email, "status": "NOT FOUND"}
            self.response.payload = dumps(empty_response)
        else:
            self.response.payload = dumps(response.json())
        """

"""

uses the following server objects

"""