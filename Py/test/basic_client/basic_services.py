import sys
sys.path.append("../../../Py/Ws/ServiceImpl")
sys.path.append("../../../Py/Ws/websocket_server")
sys.path.append("../../../Py/Ws/RootedHttpServer")

import os
import ServiceImpl
import threading

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




client_file_location = os.path.abspath("../../../Js/test/basic_client/client.html")
port = 8080
WsJsPyController = ServiceImpl.ServiceImpl(port, client_file_location,  message_router_impl(), 2)

try:

    WsJsPyController.start()
    print "Waiting for WS thread to shutdown"
    WsJsPyController.main_thread_wait_ws_shutdown()
    print "Waiting for secondary shutdown"
    if WsJsPyController.shutdown(10, False):
        print("******************************")
        print("* SERVER-SIDE TEST SUCCEEDED")
        print("******************************")
    else:
        raise "ERROR: First shutdown call failed with 4 second timeout."
except:
    print("******************************")
    if WsJsPyController.shutdown(4): # 4 second timeout
        print("* SERVER-SIDE TEST FAILED, but webservices managed to shut down.")
    else:
        print("* SERVER-SIDE TEST FAILED, with fun webservices orphaned, unfortunately.")
        print("* Please kill orphaned web services.")
    print("******************************")
    raise
