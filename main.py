from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time

listenPort = 8000 # to do: argument here
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
        for _ in range(59): # to do: argument here
            self.wfile.write(body.encode())
            time.sleep(1)
        self.wfile.write(tail.encode())
def startTarpit(server=HTTPServer, response=HTTPResponse, port=listenPort):
    listenAddress = ('', listenPort) #to do: argument here
    httpd = server(listenAddress, response)
    logging.info(f'now listening on {listenAddress}')
    httpd.serve_forever()

startTarpit()