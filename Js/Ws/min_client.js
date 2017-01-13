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
            that.onMessage(e.data);
        };

        ws.onclose = function () {
            that.onClose();
        };

        ws.onerror = function (e) {
            that.onError(e);
        };
    };

    that.send = function(msgObject) {
        if(ws) {
            // Always marshal data into JSON
            ws.send(JSON.stringify(msgObject));
        } else {
            ws.onerror(new Error("Trying to send a message on uninitialized websocket object."))
        }
    };

    return that;
}