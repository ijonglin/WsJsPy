import sys
sys.path.append("../../../Py/Ws/ServiceImpl")
sys.path.append("../../../Py/Ws/websocket_server")
sys.path.append("../../../Py/Ws/RootedHttpServer")

import os
import ServiceImpl
import threading
import argparse

print("Starting basic client test...")

# TODO(ijonglin): Move bootstrap implementation inside of bootstrap_server code
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
port = 8888

parser = argparse.ArgumentParser()
parser.add_argument(
	'--use_https', default = False, type = int,
	help = 'Start up main WsJsPy Server with self-signed HTTPS'
	)
parser.add_argument(
	'--start_browser', default = False, type = int,
	help = 'Automatically start browser within Python'
	)
args = parser.parse_args()

use_https_version = (args.use_https ==  1) # Change to True if you want to try the HTTPS version.
start_browser = (args.start_browser == 1)

if use_https_version:
    print "Running HTTPS Version of WsJsPy Service"
    # HTTPS Version of the Service.  Requires some set-up.
    WsJsPyController = ServiceImpl.ServiceImpl(port, client_file_location,  message_router_impl(), 2,
                                           server_certfile='wsjspy-selfsigned.pem', browser_pref='google-chrome',
                                           start_browser = start_browser)
else:
    print "Running plain ol' HTTP Version of WsJsPy Service"
    # Plain ol' HTTP Version of the Service
    WsJsPyController = ServiceImpl.ServiceImpl(port, client_file_location,  message_router_impl(), 2,
                                           start_browser = start_browser)

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
