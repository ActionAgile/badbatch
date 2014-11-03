import json

import falcon
from wsgiref import simple_server

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from models import Recipient, RecipientStore, InvalidUKMobileNumberException

rs = RecipientStore()

class RecipientResource:

    def on_post(self, req, resp):
        """Handles POST requests"""
        payload = json.loads(req.stream.read())   
        logger.debug('Recieved {} '.format(payload))
        try: 
            r = Recipient(payload)
            r.validate()
            key = rs.add(r)
            logger.debug('Added recipient at {}'.format(key))
        except InvalidUKMobileNumberException, e:
            logger.error(e)
            raise falcon.HTTPBadRequest(
            'You need to supply a valid UK mobile number.',
            'See docs for more details.')


api = falcon.API()
recipient_end_point = RecipientResource()
api.add_route('/recipient', recipient_end_point)


if __name__ == '__main__':
    logger.debug('Starting server on http://127.0.0.1:8000...')
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
