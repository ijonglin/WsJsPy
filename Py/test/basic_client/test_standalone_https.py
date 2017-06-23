"""
Basic Python code to run a HTTP Server and test the correctness of the self-signed certificate.
"""
import BaseHTTPServer, SimpleHTTPServer
import ssl

# Snippet of Python code from https://www.piware.de/2011/01/creating-an-https-server-in-python/
# to test to make sure the certificate is valid.
httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='wsjspy-selfsigned.pem', server_side=True)
httpd.serve_forever()
