import threading
import time
import bottle
from coverage import Coverage, CoverageData


class Jtag(threading.Thread):
    """Jtag class """
    def __init__(self, coverage: Coverage):
        super(Jtag, self).__init__()
        self.coverage = coverage

    def run(self):
        app = bottle.Bottle()

        @app.route('/')
        def hello():
            cov: CoverageData = self.coverage.get_data()
            return str(cov.lines('/Users/lyyyuna/gitup/test/test.py'))

        app.run(host='localhost', port=8082, quiet=True)
