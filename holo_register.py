# stdlib
from contextlib import closing
from sqlalchemy.sql import text

# Zato
from zato.server.service import Service
from zato.common import ZatoException


class HoloHost(Service):
    def handle(self):
        try:
            out_name = 'holohost'
            self.logger.info(type(self.request.raw_request))
            req_data = self.request.bunchified()
            select = text(
                """ SELECT CASE WHEN EXISTS (SELECT * FROM holohost WHERE email = '%s' ) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END""" % (
                    req_data['email']))

            self.logger.info(req_data['tos_agree'])
            insert = text(
                """insert into holohost(email, tos_agree, created_on) values ('%s', '%r', now()::timestamp without time zone)""" % (
                    req_data['email'], req_data['tos_agree']))
            with closing(self.outgoing.sql.get(out_name).session()) as session:
                for result in session.execute(select):
                    self.logger.info('Email already exists %r' % result)
                    self.logger.info(type(result[0]))
                    if result[0] == u'0':
                        session.execute(insert)
                        ins_result = session.commit()
                        self.logger.info(ins_result)
                        self.response.payload = {
                            'success' : req_data['email'] + ' is registered as a Holo Host'
                        }
                    if result[0] == u'1':
                        self.response.payload = {
                            'error': 'Bad Request ' + req_data['email'] + ' already exists as Holo Host account'
                        }
        except ZatoException, e:
            self.logger.warn('Caught an exception %s', e.message)




"""
1. create db holohost
2. create table with schema
3. grant user permissions on tables in new db
4. create connection to db
5. create rest channel
6. create kong proxy endpoint /holoreg

example request

curl -i -X POST proxy.holo.host/holohost/register -d '{"email":"samuel.roseabcd@gmail.com", "tos_agree": true}'
"""