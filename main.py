from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
import argparse

parser = argparse.ArgumentParser(
    prog="python-http",
    description="a horrible name for a little test project. it's an HTTP tarpit that sends an html page slowly over some time",
    epilog="I would like to thank the academy"
)
parser.add_argument("-p", "--port", help="Port number (default: 8000)", required=False)
parser.add_argument("-a", "--address", help="Listen address", required=False)
parser.add_argument("-t", "--tar", help="Tarpit depth (default: 59). One HTML element each second.", required=False)
arguments = parser.parse_args()
listenPort = int(arguments.port) or 8000
listenAddress = (arguments.address or '', listenPort)
tarDepth = int(arguments.tar) or 59

head = "<!DOCTYPE html><html><head><title>The slow page</title><body>"
body = "<p>This is going to take a while...</p>"
tail = "<p>Done, thank you for your patience and please visit us again.</p></body></html>"

class HTTPResponse(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f'connected to {self.client_address[0]}')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('X-Forwarded-For', self.client_address[0])
        self.end_headers()
        self.wfile.write(head.encode())
        for _ in range(tarDepth):
            self.wfile.write(body.encode())
            time.sleep(1)
        self.wfile.write(tail.encode())
def startTarpit(server=HTTPServer, response=HTTPResponse, port=listenPort):
    httpd = server(listenAddress, response)
    logging.info(f'now listening on {listenAddress}')
    httpd.serve_forever()

startTarpit()