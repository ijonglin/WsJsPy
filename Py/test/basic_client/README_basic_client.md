# /basic_client

# Overview:

*  Show the minimal infrastructure to show complete WsJsPy functionality
    * Backend Services run within single Python script
    * Frontend UI run within a HTML5 webpage served by the Backend Services
    * Embedded Websocket Server in Python provides internal transport layer between the two
*  Single Start-up through Python script, when run on a desktop environment
    * Servers are started on localhost
    * Client Browser is started via Python module *webbrowser*
*  (Optional) Implementation for HTTPS version of infrastructure.
    * Turned on by default due to different browser requirements on self-signed certificates
    
# Instructions
To execute, open a terminal, cd into WsJsPy/Py/test/basic_client directory and run the following command:
    
```bash
python basic_services.py
```

To run HTTPS version of the infrastructure, modify the *use_https_version* variable in *basic_services.py* script, 
and follow the instructions above.
