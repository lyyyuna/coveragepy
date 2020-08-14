import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from coverage import Coverage, CoverageData


class Jtag(threading.Thread):
    """Jtag class """
    def __init__(self, coverage: Coverage):
        super(Jtag, self).__init__()
        self.coverage = coverage

    def run(self):
        cov = self.coverage
        class MyHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = urlparse(self.path).path
                query = urlparse(self.path).query
                if path == '/v1/lines':
                    name = parse_qs(query).get('file')
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    data = cov.get_data()
                    self.wfile.write(str(data.lines('/Users/lyyyuna/gitup/test/test.py') + name).encode())
                else:
                    self.send_error(404)
        server_address = ('', 8000)
        httpd = ThreadingHTTPServer(server_address, MyHandler)
        httpd.serve_forever()