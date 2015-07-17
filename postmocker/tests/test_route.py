import gevent
import gevent.monkey

gevent.monkey.patch_all()

import json
import re
import unittest
import os

from postmocker.appbuilder import Route

sample_collection_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_collection.json')

class RouteTests(unittest.TestCase):

    def setUp(self):
        with open(sample_collection_path, 'r') as sample_collection_fp:
            self.collection = json.load(sample_collection_fp)

    def test_route(self):
        request = self.collection['requests'][0]  # Sample collection has only one request.
        response = request['responses'][0]  # Sample collection has only one response

        route = Route(request, response)

        self.assertEquals(route.name, re.sub('[^A-Za-z0-9]+', '', request['name']))
        self.assertEquals(route.request_query_args, {u'hey': [u'lo']})
        self.assertEquals(route.request_body_args, {u'people': [u'bill', u'steve', u'bob']})
        self.assertEquals(route.request_method, 'POST')
        self.assertEquals(route.request_path, '/api/jsonBlob')

        self.assertEquals(route.response_code, 201)
        self.assertEquals(len(route.response_headers), 12)
        self.assertEquals(route.response_text, '{\"people\":[\"bill\",\"steve\",\"bob\"]}')
