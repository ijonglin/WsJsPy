import webbrowser
import urllib
import threading
import json
import websocket_server

class ServiceImpl:
    MESSAGE_TYPE_KEY = "MessageType"
    MESSAGE_PAYLOAD_KEY = "MessagePayload"
    WSJSPY_BOOTSTRAP_KEY = "WSJSPY_BOOTSTRAP"

    def __init__(self, port, client_file_location, message_router):
        ws_url = "ws://localhost:" + str(port)
        self.ws_server = websocket_server.WebsocketServer(port)
        self.ws_server.set_fn_message_received(self.message_received)
        self.message_router = message_router
        self.message_count = 0

        def delay_open_ui(file_location):
            webbrowser.open("file://" + file_location + "?"+ServiceImpl.WSJSPY_BOOTSTRAP_KEY+"="
                            + urllib.quote(ws_url, safe=""))

        # self.thread_browser = threading.Timer(3, lambda: delay_open_ui(client_file_location))
        self.thread_wsserver = threading.Timer(0, lambda: self.ws_server.run_forever())
        delay_open_ui(client_file_location)

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
        message_payload =parsed_message[ServiceImpl.MESSAGE_PAYLOAD_KEY]
        if message_name in self.message_router:
            self.message_router[message_name](self, message_payload)
        else:
            self.router_fallback(message_name, message_payload)

    def start(self):
        # Note that there's a race condition between websocket server and browser
        self.thread_wsserver.start()
        # TODO: Need to start a local websocket client and connect before start the webbrowser
        # self.thread_browser.start()

    def wait_for_server_exit(self, timeout = None):
        self.thread_wsserver.join(timeout)

    def send_raw(self, message):
        self.ws_server.send_message_to_all(message)

    def shutdown(self):
        self.ws_server.shutdown()

    def send(self, message, payload):
        self.send_raw(
            self.marshall({
                ServiceImpl.MESSAGE_TYPE_KEY: message,
                ServiceImpl.MESSAGE_PAYLOAD_KEY: payload
            })
        )
