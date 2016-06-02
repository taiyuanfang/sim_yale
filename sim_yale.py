import SimpleHTTPServer, SocketServer
import urlparse
import os
import signal
import sys


def signal_handler(signal, frame):
    httpd.shutdown
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

        # Parse query data & params to find out what was passed
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)

        print queryParsed

        # request is either for a file to be served up or our test
        if parsedParams.path == "/test":
            self.processMyRequest(queryParsed)
        else:
            # Default to serve up a local file
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self);

    def processMyRequest(self, query):
        build_path = "build/"
        met = query["met"][0]
        did = query["did"][0]
        pwd = query["pwd"][0]
        cmd = build_path + met + " " + did + " " + pwd
        print "cmd:", cmd
        os.system(cmd)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(query);
        self.wfile.close();


PORT = 8000
Handler = MyHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
