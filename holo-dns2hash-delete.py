from zato.server.service import Service
from json import dumps
import httplib

class HoloDns2HashDelete(Service):
    def checkKey(self, d, key):
        return key in d

    def kvdb_get( self, system, key ):
        # kvdb
        service = 'zato.kvdb.data-dict.dictionary.get-value-list'
        request = { "system":system, "key":key }
        response = self.invoke( service, request )
        return response["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]


    def handle(self):
        # miscellaneous logging
        self.logger.info(self.request.raw_request)
        self.logger.info('cid:[{}]'.format(self.cid))
        # prep data
        data = self.request.bunchified()
        self.logger.info(data)

        # exit if missing incoming data
        if not self.checkKey(data, 'kv_key'):
            response = {"error": "request must contain a kv store key"}
            self.response.status_code = httplib.BAD_REQUEST
            self.response.payload = dumps(response)
            return

        auth_email = self.kvdb_get( 'cloudflare', 'auth_email' )
        self.logger.info(auth_email)
        auth_key = self.kvdb_get( 'cloudflare', 'auth_key' )
        self.logger.info(auth_key)
        # Headers the endpoint expects
        headers = {'X-Auth-Email':auth_email, 'X-Auth-Key':auth_key, 'Content-Type':'application/json'}

        account = self.kvdb_get( 'cloudflare', 'account' )
        self.logger.info(account)
        namespace = self.kvdb_get( 'cloudflare', 'kvstore_dns2hash' )
        self.logger.info(namespace)
        kv_key = data.kv_key
        # params
        params = {"account":account, "namespace":namespace, "kv_key":kv_key}
        # payload
        payload = {}

        # Obtains a connection object
        conn = self.outgoing.plain_http['cloudflare-kvstore-dns2hash-delete'].conn

        # Invoke the resource providing all the information on input
        try:
            response = conn.delete(self.cid, params, headers=headers)
        except:
            response = {"error": "something broke"}
            self.response.status_code = httplib.BAD_GATEWAY # 502
            self.response.payload = dumps(response)
            return
        else:
            self.response.payload = dumps(response.json())
            return

"""

uses the following server objects

outconn:cloudflare-kvstore-dns2hash-delete:
    https://api.cloudflare.com
    /client/v4/accounts/{account}/storage/kv/namespaces/{namespace}/values/{kv_key}
    Cloudflare API

"""
