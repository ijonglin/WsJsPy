import websocket_server
import json


class WsJsPyBootstrapper:
    """
    Build up a minimal JSON message routing protocol on top of basic Websocket server
    for basic RPC string to string calls to the Python layer.  It's a simple stateful service
    that interprets all messages as implementation specific bootstrap messages.  When bootstrap
    is completed, then the server passes messages directly to the dictionary functional map provided
    on the constructor.
    TODO(ijonglin): Add JSON Schema protocol for run-time messaging checking.
    TODO(ijonglin): Unpacked message should also be decoded as JS dictionary.
    """
    def __init__(self, service_handler):
        """
        :param service_handler: a dictionary of functional handlers, where the key maps to the message as a string
        :type service_handler:
        """
        self.service_handler = service_handler
        self.ws_server = websocket_server.WebsocketServer(8080)
        self.ws_server.set_fn_message_received(self.message_handler)
        self.bootstrap_passed = False
        self.validator = {}

    def bootstrap_handler(self, client, server, message):
        """
        Higher priority message handler that intercepts calls before they get to the service handler layer.
        :param client: WebSocket client reference
        :type client: Based on the underlying websocket_server implememtation
        :param server: WebSocket server reference
        :type server: Based on the underlying websocket_server implememtation
        :param message: Message from client
        :type message: String
        :return: None
        :rtype: None
        """
        pass

    def message_handler(self, client, server, message):
        """
        Handler for the implementation-specific version of the websocket server.
        TODO(ijonglin): Introduce an implementation abstraction layer for the particular WebSocket server.
        :param client: WebSocket client reference
        :type client: Based on the underlying websocket_server implememtation
        :param server: WebSocket server reference
        :type server: Based on the underlying websocket_server implememtation
        :param message: Message from client
        :type message: String
        :return: None
        :rtype: None
        """
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
