from zato.server.service import Service
from json import dumps
from anyjson import loads


class HoloZtAuth(Service):
    def checkKey(self, d, key):
        return key in d

    def handle(self):
        data = self.request.bunchified()
        service = 'zato.kvdb.data-dict.dictionary.get-value-list'
        ddrequest = {'system': 'zerotier', 'key': 'network_id'}
        ddresponse = self.invoke(service, ddrequest)
        network_id = ddresponse["zato_kvdb_data_dict_dictionary_get_value_list_response"][0]["name"]
        # self.logger.info(network_id)
        params = {'network_id': network_id, 'member_id': data['member_id']}
        # self.logger.info(params)
        # # Obtains a connection object
        conn = self.outgoing.plain_http['zerotier'].conn
        #
        # # Invoke the resource providing all the information on input
        response = conn.get(self.cid, params)
        res_data = loads(response.text)
        new_data = dict(res_data.items())
        # self.logger.info(res_data)
        # self.logger.info(res_data['config']['authorized'])
        new_data['config']['authorized'] = True
        # self.logger.info(new_data)
        newconn = self.outgoing.plain_http['zerotier'].conn
        newparams = {'network_id': network_id, 'member_id': data['member_id']}
        auth = newconn.post(self.cid, new_data, params=newparams)
        # self.logger.info(auth.json())
        self.response.payload = dumps(auth.json())


"""

uses the following server objects

outconn:zerotier:
    https://my.zerotier.com    
    /api/network/{network_id}/member/{member_id}	
    API/key 
    zerotier	

rest-channel:zt-auth
    	/zt-auth
    	holo-init-email.holo-init-email
    	apikey (a generic one I create that all rest channels can use)


"""