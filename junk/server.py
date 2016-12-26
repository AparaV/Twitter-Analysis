import sys
import threading
import time
import webbrowser

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


class Server:
    def __init__(self, port=8000):
        self._initserver(port)

    def openbrowser(self, url):
        webbrowser.open_new_tab(url)
        self.exitserver()

    def exitserver(self):
        q = str(raw_input('Hit Q to exit server.\n'))
        while q != 'q':
            q = str(raw_input())
        print ('Shutting down server at port', self.PORT)
        self.httpd.shutdown()
        sys.exit(0)

    def _initserver(self, port):
        self.PORT = 8000
        self.httpd = HTTPServer(('localhost', self.PORT), SimpleHTTPRequestHandler)
        print ('Serving at port', self.PORT)
        self.th = threading.Thread(target=self.httpd.serve_forever)
        self.th.daemon = True
        self.th.start()
        time.sleep(5)