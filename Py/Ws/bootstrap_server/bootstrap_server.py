import websocket_server
import json


class WsJsPyBootstrapper:
    def __init__(self, service_handler):
        self.service_handler = service_handler
        self.ws_server = websocket_server.WebsocketServer(8080)
        self.ws_server.set_fn_message_received(self.message_handler)
        self.bootstrap_passed = False
        self.validator = {}

    def bootstrap_handler(self, client, server, message):
        pass

    def message_handler(self, client, server, message):
        unpacked_message = json.loads(message)
        print "MESSAGE:", message
        if self.bootstrap_passed:
            if (self.bootstrap_handler["action"] in self.service_handler):
                self.bootstrap_handler[unpacked_message["action"]](unpacked_message["params"])
            else:
                print
                "This service received an request of ", unpacked_message["action"], " that can't handle.  Ignoring."
        else:
            if (unpacked_message["action"] in self.service_handler):
                self.service_handler[unpacked_message["action"]](unpacked_message["params"])
            else:
                print
                "This service received an request of ", unpacked_message["action"], " that can't handle.  Ignoring."
