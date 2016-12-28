/**
 * Created by ijonglin on 12/28/16.
 */

function WsJsPyMinimalInit() {
    var that = this;
    var ws;
    // Connect to Web Socket

    // default implemntations.
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
        console.log("WS: Successfully closed.");
    };

    that.init = function() {
        ws = new WebSocket("ws://localhost:8080/");
        // Set event handlers.
        ws.onopen = function () {
            that.onOpen();
        };

        ws.onmessage = function (e) {
            // e.data contains received JSON-encoded string.
            parsed_data = JSON.parse(e.data);
            that.onMessage(e.data);
        };

        ws.onclose = function () {
            that.onClose();
        };

        ws.onerror = function (e) {
            that.onError(e);
        };
    };

    that.send = function(msg) {
        if(ws) {
            ws.send(msg);
        } else {
            // throw Error
        }
    }

    return that;
}