import posixpath
import os
import ssl
import json
from urllib.parse import urlparse

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler as SimpleHTTPRequestHandler


class RootedHTTPServer(HTTPServer):
    """
    Simple Subclass that serves a read-only file system directory onto HTTP where Python is running. Pages that are
    then locally created within the file system can be used, as the basis for WsJsPy application UI.  Primarily,
    just create an internal class property that is available to the subclassed RootedHTTPRequestHandler handler.
    Currently, this implementation is tested only for Linux and MacOS type file systems, but should be written to
    handle WindowOS systems.
    TODO:  Test this function for Window-type filesystems.
    """

    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.base_path = base_path


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server_class):
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    def do_GET(self):
        """
        Basic fileserving GET implementation for this simple web server.

        :return:  side-effect, actions to create correct response 404 or the 200 result
                  of the file to be served.
        """
        fs_path = posixpath.normpath(self.server.base_path +"/"+ urlparse(self.path).path)
        if not os.path.exists(fs_path):
            self.send_response(404)
            return
        with open(fs_path, "r") as fout:
            response=fout.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

def ConstructRootedHttpServer(server, port, directory_to_serve):
    """
    Factory function that returns an implementation of HTTP Server that
    serves a specific subdirectory on the filesystem where Python is
    running.
    :param server: Name of server address
    :type server: String
    :param port: Port number to server the directory
    :type port: Int
    :param directory_to_serve:
    :type directory_to_serve: String
    :return: Instantiated RootedHTTPServer with RootedHTTPRequestHandler
    :rtype: RootedHTTPServer
    """
    server_address = (server, port)
    return RootedHTTPServer(directory_to_serve, server_address, RootedHTTPRequestHandler)


def ConstructRootedSecureHttpServer(server, port, directory_to_serve, certfile):
    server = ConstructRootedHttpServer(server, port, directory_to_serve)
    server.socket = ssl.wrap_socket(server.socket, certfile=certfile, server_side=True)
    return server
