import json
import logging
import re
import urlparse

from flask import Flask

logger = logging.getLogger(__name__)

BLACKLISTED_HEADERS = [
    # These are blacklisted because they relate to the mode of transport.
    'content-length',
    'transfer-encoding',
    'content-encoding'
]


class Route(object):
    def __init__(self, req, response):
        self.name = re.sub('[^A-Za-z0-9]+', '', req['name'])
        self._set_request(req)
        self._set_response(response)

    def _set_request(self, req):
        # Query String
        url = req['url']
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
        parsed_url = urlparse.urlparse(url)
        if parsed_url.query:
            self.request_query_args = urlparse.parse_qs(parsed_url.query)

        # Body params
        if req['dataMode'] == 'urlencoded' or req['dataMode'] == 'params':
            self.request_body_args = dict([(arg['key'], arg['value']) for arg in req['data']])
        else:
            try:
                self.request_body_args = json.loads(req['rawModeData'])
            except ValueError:
                # The raw request body is not something we can process. Store it, but do nothing with it.
                self.request_body_args = req['rawModeData']

        # Method
        self.request_method = req['method']
        logger.debug('Set request method to %s', req['method'])

        # Path
        path = parsed_url.path
        segments = path.split('/')
        final_segments = []

        # Handle any path variables
        path_variables = req.get('pathVariables', {})

        for segment in segments:
            final_segment = path_variables.get(segment[1:], segment)
            final_segments.append(final_segment)

        self.request_path = '/'.join(final_segments) or '/'
        logger.debug('Set path to %s', self.request_path)

    def _set_response(self, response):
        self.response_code = response['responseCode']['code']
        self.response_headers = dict([(header['key'], header['value'])
                                      for header in response['headers']
                                      if header['key'].lower() not in BLACKLISTED_HEADERS])
        self.response_text = response['text']

    def __call__(self):
        return self.response_text, self.response_code, self.response_headers.items()


class AppBuilder(object):
    def __init__(self, collection):
        self.app = Flask(__name__)
        self.collection = collection
        self._valid_routes = self.get_valid_routes()
        logger.debug('Creating a WSGI app for collection: %s', collection['name'])

    def get_valid_routes(self):
        routes = []
        for req in self.collection['requests']:
            if req['responses']:
                logger.debug('Found a valid request: %s', req['url'])
                response = req['responses'][0]  # Consider only the first response
                routes.append(Route(req, response))
        return routes

    def build_app(self):
        for route in self._valid_routes:
            self.app.add_url_rule(route.request_path, route.name, route, methods=[route.request_method])
        return self.app
