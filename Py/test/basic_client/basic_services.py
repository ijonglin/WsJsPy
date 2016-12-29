import json
import min_server

print("Starting robot service...")

# Set up the message handlers and link back to the simulation service
def message_received(client, server, message):
    message_object = json.loads(message)
    print("MESSAGE:", message_object)

server = min_server.MinServer("../../../Js/test/basic_client/client.html", message_received)


