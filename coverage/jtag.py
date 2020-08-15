import threading
import time
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from coverage import Coverage, CoverageData


class Jtag(threading.Thread):
    """Jtag class """
    def __init__(self, coverage: Coverage, host: str, port: str):
        super(Jtag, self).__init__()
        self.coverage = coverage
        self.host = host
        self.port = port

    def run(self):
        cov = self.coverage
        class JtagHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # no logging, keep stdout/stderr quiet
                return

            def do_GET(self):
                path = urlparse(self.path).path
                query = urlparse(self.path).query
                if path == '/v1/lines':
                    name = parse_qs(query).get('file', None)
                    if name is None:
                        self.send_error(404)
                        return
                    data = cov.get_data()
                    lines = data.lines(name[0])
                    if lines is None:
                        self.send_error(404)
                        return

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(lines).encode())
                else:
                    self.send_error(404)
        server_address = (self.host, int(self.port))
        httpd = ThreadingHTTPServer(server_address, JtagHandler)
        httpd.serve_forever()