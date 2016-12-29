import threading
import webbrowser
import websocket_server


class MinServer:
    def __init__(self, client_html_location, message_handler):
        print("Listening for Websockets request on port 8080")
        self.ws_server = websocket_server.WebsocketServer(8080)
        self.ws_server.set_fn_message_received(message_handler)

        # Slight race condition here on start-up
        self.delay_open_ui(client_html_location)
        self.ws_server.run_forever()

    def _delay_open_ui(self, client_html_location):
        webbrowser.open(client_html_location)

    def delay_open_ui(self, client_html_location):
        t = threading.Timer(3, lambda: self._delay_open_ui(client_html_location))
        t.start()
