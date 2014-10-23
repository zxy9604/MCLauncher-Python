import json
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


path = "."

class RequestHandler(BaseHTTPRequestHandler):
    def _writeheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def do_GET(self):
        self._writeheaders()
        self.wfile.write(json.dumps(os.listdir(path)).encode())

serveraddr = ('127.0.0.1', 8884)
srvr = HTTPServer(serveraddr, RequestHandler)
srvr.serve_forever()
