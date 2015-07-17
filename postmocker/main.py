import logging
import gevent

from gevent.pywsgi import WSGIServer, WSGIHandler
from postmocker.appbuilder import AppBuilder

logger = logging.getLogger(__name__)

class LoggingWSGIHandler(WSGIHandler):

    def __init__(self, socket, address, server, *args, **kwargs):
        self.logger = logging.getLogger('http')
        super(LoggingWSGIHandler, self).__init__(socket, address, server)

    def log_request(self):
        self.logger.debug(self.format_request())


class PostMocker(object):

    def __init__(self, collection, port):
        self.server_greenlet = None
        self.collection = collection
        self.server = None
        self.port = port
        self.builder = AppBuilder(collection)
        self.app = None

    def start(self):
        self.app = self.builder.build_app()
        self.server = WSGIServer(('', self.port), self.app, handler_class=LoggingWSGIHandler)
        self.server_greenlet = gevent.spawn(self.server.serve_forever)

        while self.server.server_port == 0:
            gevent.sleep(0)  # Wait until the server has started
        logger.info('PostMocker listening on port: %s', self.server.server_port)
        return self.server_greenlet

    def stop(self):
        logger.info('Stopping')
        self.server.stop()
