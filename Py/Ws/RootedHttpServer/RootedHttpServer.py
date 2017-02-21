import posixpath
import argparse
import urllib
import os

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer


class RootedHTTPServer(HTTPServer):
    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Remove any query parameters
        path = path.split('?')[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

def ConstructRootedHttpServer(server, port, directory_to_serve):
    server_address = (server , port)
    return RootedHTTPServer(directory_to_serve, server_address, RootedHTTPRequestHandler)
