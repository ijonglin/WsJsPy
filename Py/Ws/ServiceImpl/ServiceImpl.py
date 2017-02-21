import webbrowser
import urllib
import threading
import json
import websocket_server
import RootedHttpServer
import os


class ServiceImpl:
    MESSAGE_TYPE_KEY = "MessageType"
    MESSAGE_PAYLOAD_KEY = "MessagePayload"
    WSJSPY_BOOTSTRAP_KEY = "WSJSPY_BOOTSTRAP"

    def __init__(self, port, client_file_location, message_router,
                 dir_levels_to_serve = 0,
                 start_browser=True,
                 serve_ui=True
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

    def append_bootstrap_parameter(self, url, ws_url):
        return url + "?" + ServiceImpl.WSJSPY_BOOTSTRAP_KEY + "=" + urllib.quote(ws_url, safe="")

    def convert_to_file_url(self, file_location, ws_url):
        return self.append_bootstrap_parameter("file://" + file_location, ws_url)

    def delay_open_ui(self, url_to_open):
        browser = webbrowser.get('firefox')
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
        self.ui_file_server = RootedHttpServer.ConstructRootedHttpServer(
            "localhost", 8008, dir_to_serve)
        self.thread_ui_file_server =threading.Timer(0, lambda: self.ui_file_server.serve_forever())
        self.thread_ui_file_server.start()
        return "http://localhost:8008/"+dir_to_add+"/"+os.path.basename(file_location)

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
            print "You need to open the link in "
        # self.thread_browser.start()


    def wait_for_server_exit(self, timeout=None):
        self.thread_wsserver.join(timeout)

    def send_raw(self, message):
        self.ws_server.send_message_to_all(message)


    def shutdown(self):
        if self.serve_ui:
            self.thread_ui_file_server.cancel()
        self.ws_server.shutdown()

    def send(self, message, payload):
        self.send_raw(
            self.marshall({
                ServiceImpl.MESSAGE_TYPE_KEY: message,
                ServiceImpl.MESSAGE_PAYLOAD_KEY: payload
            })
        )
