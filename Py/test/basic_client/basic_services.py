import websocket_server
import webbrowser
import json
import threading

print("Starting robot service...")

# Set up the message handlers and link back to the simulation service
def message_received(client, server, message):
    print("MESSAGE:", message)

print("Listening for Websockets request on port 8080")
ws_server = websocket_server.WebsocketServer(8080)
ws_server.set_fn_message_received(message_received)

# Slight race condition here on start-up
def delay_open_ui():
    webbrowser.open("../../../Js/test/basic_client/client.html")

t = threading.Timer(3, delay_open_ui)
t.start()
ws_server.run_forever()
