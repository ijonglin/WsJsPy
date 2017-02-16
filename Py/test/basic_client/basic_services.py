import os
import ServiceImpl

print("Starting basic client test...")

def message_router_impl():
    def raw_handler(server, message):
        if message == "BOOTSTRAP":
            server.send("RAW", "BOOTSTRAP_RESPONSE")
        elif message == "TEST_MESSAGE":
            server.send("RAW", "TEST_RESPONSE")
            server.shutdown()
        else:
            server.send("RAW",
                        {
                            "EchoMessage": message,
                            "TransmitMessage": "Unhandled raw message!",
                        })
    return  {
        "RAW": raw_handler
    }

client_file_location = os.getcwd() + "/../../../Js/test/basic_client/client.html"
port = 8080
WsJsPyController = ServiceImpl.ServiceImpl(port, client_file_location, message_router_impl())

try:

    WsJsPyController.start()
    WsJsPyController.wait_for_server_exit()
    print("SERVER-SIDE TEST SUCCEEDS, if it gets to this point w/o exceptions.")
except:
    WsJsPyController.shutdown()
    WsJsPyController.wait_for_server_exit()
    print("SERVER-SIDE TEST FAILED.")
    raise
