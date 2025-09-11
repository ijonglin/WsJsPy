/**
 * Created by ijonglin on 12/28/16.
 */

function WsJsPyMinimalInit() {
    var that = this;
    var ws;
    // Connect to Web Socket

    // default implementations.
    that.onOpen = function () {
        console.log("WS: Successfully opened.");
    };

    that.onMessage = function (msg) {
        console.log("WS: Received message:"+msg);
    };

    that.onClose = function () {
        console.log("WS: Successfully closed.");
    };

    that.onError = function () {
        console.log("WS: Error.");
    };

    that.onReady = function () {
        console.log("WS: Ready.");
    };

    that.init = function(ws_bootstrap_url) {
        if(ws_bootstrap_url===undefined) {
            // Written by Chris Coyier from https://css-tricks.com/snippets/javascript/get-url-variables/
            function getQueryVariable(variable) {
                var query = window.location.search.substring(1);
                var vars = query.split("&");
                for (var i = 0; i < vars.length; i++) {
                    var pair = vars[i].split("=");
                    if (pair[0] == variable) {
                        return pair[1];
                    }
                }
                return (false);
            };

            ws_bootstrap_url = decodeURIComponent(getQueryVariable("WSJSPY_BOOTSTRAP"));
        }


        console.log("WSJSPY Bootstrap =" + ws_bootstrap_url)

        function readyWebSocket(ws_ready) {
            // Set event handlers.
            ws_ready.onopen = function () {
                that.onOpen();
            };

            ws_ready.onmessage = function (e) {
                that.onMessage(e.data);
            };

            ws_ready.onclose = function () {
                that.onClose();
            };

            ws_ready.onerror = function (e) {
                that.onError(e);
            };

            that.onReady();
        };

        function retryWebsocketInit(retryAttempts) {
            try {
                ws = new WebSocket(ws_bootstrap_url);
                readyWebSocket(ws);
            } catch(err) {
                console.log("Retrying to open Websockets: "+retryAttempts+" attempts remaining.");
                setTimeout(function() { retryWebsocketInit(retryAttempts-1);} , 250);
            }
        };
        retryWebsocketInit(10);
    };

    that.close = function() {
        if(ws) {
            ws.close();
        }
    }

    that.send = function(msg) {
        if(ws) {
            // Minimal client doesn't do any marshalling
            ws.send(msg)
        } else {
            ws.onerror(new Error("Trying to send a message on uninitialized websocket object."))
        }
    };

    return that;
}