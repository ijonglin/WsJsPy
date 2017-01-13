import websocket_server
import webbrowser
import json
import threading

print("Starting robot service...")

def send_json_wrapped(client, server, message):
    server.send_message(client, json.dumps(message));

message_count = 0

# Set up the message handlers and link back to the simulation service
def message_received(client, server, message):
    global message_count
    message_count = message_count + 1
    print("MESSAGE[{0}] -- {1}".format(message_count, message))
    parsed_message = json.loads(message)
    if(parsed_message["MessageType"] == "RAW" and parsed_message["MessagePayload"] == "BOOTSTRAP"):
        send_json_wrapped(client, server, { "MessageType": "RAW",
                                            "MessagePayload": "BOOTSTRAP_RESPONSE"
                                                }
                          )
        return

    if(parsed_message["MessageType"] == "RAW" and parsed_message["MessagePayload"] == "TEST_MESSAGE"):
        send_json_wrapped(client, server, { "MessageType": "RAW",
                                            "MessagePayload": "TEST_RESPONSE"
                                            }
                          )
        server.shutdown()
        return

    # Default service
    send_json_wrapped(client, server, { "MessageType": "RAW",
                                        "MessagePayload": {
                                            "EchoMessage": message,
                                            "TransmitMessage": "HIYA!",
                                            "MessageCount": message_count
                                            }
                                        }
    )

print("Listening for Websockets requests on port 8080")
ws_server = websocket_server.WebsocketServer(8080)
ws_server.set_fn_message_received(message_received)

# Slight race condition here on start-up
def delay_open_ui():
    webbrowser.open("../../../Js/test/basic_client/client.html")

t = threading.Timer(3, delay_open_ui)
t.start()
ws_server.run_forever()
