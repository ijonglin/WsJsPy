import os
import posixpath
import urllib
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


class RootedHTTPServer(HTTPServer):
    """
    Simple Subclass that serves a read-only file system directory onto HTTP where Python is running. Pages that are
    then locally created within the file system can be used, as the basis for WsJsPy application UI.  Primarly,
    just create an internal class property that is available to the subclassed RootedHTTPRequestHandler handler.
    Currently, this implementation is tested only for Linux and MacOS type file systems, but should be written to
    handle WindowOS systems.
    TODO:  Test this function for Window-type filesystems.
    """

    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Modified request handler to move the head of the path to the
    base file path associated within the server.
    """

    def translate_path(self, path):
        """
        Translate current path of request to the filesystem specified in RootedHTTPServer class
        :param path: current path fo
        :type path: string (I assume)
        :return: path with the base path appended
        :rtype: another string (I assume)
        """
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
