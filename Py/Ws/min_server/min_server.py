import threading
import webbrowser
import websocket_server
from selenium import webdriver


class MinServer:
    """
    Simple integration of server infrastructure and web browser client from the same machine.
    In the future, this framework should be available for selenium for basic end-to-end testing.
    By placing this server in its own thread, you can control its lifetime by controlling
    the lifetime of the thread.
    """
    def __init__(self, client_html_location, message_handler, selenium_tester=None):
        print("Listening for Websockets request on port 8080")
        self.ws_server = websocket_server.WebsocketServer(8080)
        self.ws_server.set_fn_message_received(message_handler)

        # Slight race condition here on start-up
        self.selenium_tester = selenium_tester
        self.delay_open_ui(client_html_location)
        self.ws_server.run_forever()

    def _delay_open_ui(self, client_html_location):
        if(self.selenium_tester is None):
            webbrowser.open(client_html_location)
        else:
            driver = webdriver.Firefox()
            driver.get(client_html_location)
            self.selenium_tester(driver)


    def delay_open_ui(self, client_html_location):
        t = threading.Timer(3, lambda: self._delay_open_ui(client_html_location))
        t.start()
