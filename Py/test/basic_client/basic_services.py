import json
import min_server

# Set up the message handlers and link back to the simulation service
def message_received(client, server, message):
    message_object = json.loads(message)
    print("MESSAGE:", message_object)

class BasicServer:
    def __init__(self, selenium_tester=None):
        self.server = min_server.MinServer("../../../Js/test/basic_client/client.html", message_received, selenium_tester)

def main():
    server = BasicServer()

if __name__=="__main__":
    main()





