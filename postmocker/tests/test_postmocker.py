import gevent
import gevent.monkey

gevent.monkey.patch_all()

import json
import os
import unittest

from postmocker.main import PostMocker

sample_collection_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_collection.json')


class PostMockerTest(unittest.TestCase):
    def setUp(self):
        with open(sample_collection_path, 'r') as sample_collection_fp:
            self.collection = json.load(sample_collection_fp)

        self.mocker = PostMocker(collection=self.collection,
                                 port=0)  # Set port to zero so OS will give any available port.
        self.mocker.start()

    def test_run(self):
        self.assertTrue(self.mocker.server.server_port != 0)  # Ensure postmocker is able to start

        test_client = self.mocker.app.test_client()
        response = test_client.post('/api/jsonBlob')

        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.data), {'people': ['bill', 'steve', 'bob']})

    def tearDown(self):
        self.mocker.stop()
