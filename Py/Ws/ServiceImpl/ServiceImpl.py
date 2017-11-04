import webbrowser
import urllib
import threading
import json
import websocket_server
import RootedHttpServer
import os


class ServiceImpl:
    """
    Provides minimal server-side and client set of services that meet the requirement of WsJsPy Application Framework,
    as well an implementation of the bootstrap framework that talks directly to the JS Client, as specified
    in subdirectory Js/Ws/min_client.js.   Underlying ystem is assumed to have a reasonable browser installed.
    The servies provided by this object for the minimal WsJsPy system is follows:
    1.  Websocket Server (Py)
    2.  HTTP-based Fileserver (Py)
    3.  Server-based Bootstrap code (Py)
    4.  Client-based Bootstrap code (Js in /Js/Ws/client.js)
    5.  Client-based Web Browser (can be started independently from URLs in #2 or by Python on the server resources)
    """
    MESSAGE_TYPE_KEY = "MessageType"
    MESSAGE_PAYLOAD_KEY = "MessagePayload"
    WSJSPY_BOOTSTRAP_KEY = "WSJSPY_BOOTSTRAP"

    def __init__(self, port, client_file_location, message_router,
                 dir_levels_to_serve = 0,
                 start_browser=True,
                 serve_ui=True,
                 server_certfile=None,
                 browser_pref=None
                 ):
        self.ws_url = "ws://localhost:" + str(port)
        self.ws_server = websocket_server.WebsocketServer(port)
        self.ws_server.set_fn_message_received(self.message_received)
        self.message_router = message_router
        self.message_count = 0
        self.client_file_location = os.path.abspath(client_file_location)
        self.serve_ui = serve_ui
        self.start_browser = start_browser
        self.ui_file_server = None
        self.thread_ui_file_server = None
        self.dir_levels_to_serve = dir_levels_to_serve
        self.shutdown_lock = threading.Lock()
        self.server_certfile = server_certfile
        self.browser_pref = browser_pref

    def append_bootstrap_parameter(self, url, ws_url):
        """
        Append the proper bootstrap information onto the client page via a query parameter.
        Code on the JS client side will pick up the information and use it to bootstrap
        a connection to the Websocket Server provided by this service.
        :param url:  URL of the client page to be loaded into a browser
        :type url: String
        :param ws_url:  URL of the websocket server
        :type ws_url: String
        :return: URL of the client page with the Websocket URL appended with proper bootstrap parameter
        :rtype: String
        """
        return url + "?" + ServiceImpl.WSJSPY_BOOTSTRAP_KEY + "=" + urllib.quote(ws_url, safe="")

    def convert_to_file_url(self, file_location, ws_url):
        """
        Helper function to convert an absolute file location to URL that is digestable
        by a browser.   Not recommended for use in browsers, since different browsers
        have differently policies w.r.t. access of local files.  Always better to
        serve the files on the provided http server.  Only tested for Linux/MacOS type filesystems.
        :param file_location:  Absolute file location
        :type file_location: String
        :param ws_url: URL of Websocket Service
        :type ws_url: String
        :return:  URL of local client page hosted on the filesystem append with the proper bootstrap parameter.
        :rtype: String
        """
        return self.append_bootstrap_parameter("file://" + file_location, ws_url)

    def delay_open_ui(self, url_to_open):
        if self.browser_pref is None:
            browser = webbrowser.get('firefox')
        else:
            browser = webbrowser.get(using=self.browser_pref)
        if browser is None:
            browser = webbrowser.get('chrome')
        if browser is None:
            browser = webbrowser
        browser.open(url_to_open)

    def marshall(self, obj):
        return json.dumps(obj)

    def demarshall(self, message):
        return json.loads(message)


    def router_fallback(self, name, payload):
        raise RuntimeError("Unrecognized message to be routed.")


    def message_received(self, client, server, message):
        self.message_count += 1
        print("MESSAGE[{0}] -- {1}".format(self.message_count, message))
        parsed_message = json.loads(message)
        message_name = parsed_message[ServiceImpl.MESSAGE_TYPE_KEY]
        message_payload = parsed_message[ServiceImpl.MESSAGE_PAYLOAD_KEY]
        if message_name in self.message_router:
            self.message_router[message_name](self, message_payload)
        else:
            self.router_fallback(message_name, message_payload)

    def start_file_server(self, file_location, levels_to_serve):
        dir_array = os.path.dirname(file_location).split(os.path.sep)
        dir_cut_point = 0-levels_to_serve
        dir_to_add = '/'.join(dir_array[dir_cut_point:])
        dir_to_serve = '/'.join(dir_array[:dir_cut_point])
        if self.server_certfile is None:
            self.ui_file_server = RootedHttpServer.ConstructRootedHttpServer(
                "localhost", 8008, dir_to_serve)
            self.thread_ui_file_server =threading.Timer(0, lambda: self.ui_file_server.serve_forever())
            self.thread_ui_file_server.start()
            return "http://localhost:8008/"+dir_to_add+"/"+os.path.basename(file_location)
        else:
            self.ui_file_server = RootedHttpServer.ConstructRootedSecureHttpServer(
                "localhost", 8008, dir_to_serve, self.server_certfile);
            self.thread_ui_file_server =threading.Timer(0, lambda: self.ui_file_server.serve_forever())
            self.thread_ui_file_server.start()
            return "https://localhost:8008/"+dir_to_add+"/"+os.path.basename(file_location)

    def start(self):
        # self.thread_browser = threading.Timer(3, lambda: delay_open_ui(client_file_location))
        self.thread_wsserver = threading.Timer(0, lambda: self.ws_server.run_forever())

        # Note that there's a race condition between websocket server and browser
        self.thread_wsserver.start()
        # TODO: Need to start a local websocket client and connect before start the webbrowser
        url_to_open = None
        if self.serve_ui:
            ui_url_service = self.start_file_server(self.client_file_location, self.dir_levels_to_serve)
            url_to_open = self.append_bootstrap_parameter(ui_url_service, self.ws_url)
        else:
            url_to_open = self.convert_to_file_url(self.client_file_location, self.ws_url)

        if self.start_browser:
            self.delay_open_ui(url_to_open)
        else:
            print "You need to open the link in " + url_to_open
        # self.thread_browser.start()


    def send_raw(self, message):
        self.ws_server.send_message_to_all(message)

    def main_thread_wait_ws_shutdown(self,timeout=None):
        self.thread_wsserver.join(timeout)

    def shutdown(self, timeout=None, shutdown_ws_server=True):
        self.shutdown_lock.acquire()
        try:
            if self.serve_ui:
                if not self.ui_file_server is None:
                    self.ui_file_server.shutdown()
                    print "waiting on shutdown of file server"
                    self.thread_ui_file_server.join(timeout)
                    if self.thread_ui_file_server.isAlive():
                        return False
                    self.ui_file_server = None
            if not self.ws_server is None and shutdown_ws_server:
                self.ws_server.shutdown()
                print "waiting on shutdown of ws"
                self.thread_wsserver.join(timeout)
                if self.thread_wsserver.isAlive():
                    return False
                self.ws_server = None
            return True
        finally:
            self.shutdown_lock.release()


    def send(self, message, payload):
        self.send_raw(
            self.marshall({
                ServiceImpl.MESSAGE_TYPE_KEY: message,
                ServiceImpl.MESSAGE_PAYLOAD_KEY: payload
            })
        )
