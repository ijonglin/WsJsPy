/**
 * Created by ijonglin on 12/23/16.
 */
var ws;

function init() {

    // Connect to Web Socket
    ws = new WebSocket("ws://localhost:8080/");

    // Set event handlers.
    ws.onopen = function () {
        output("onopen");
    };

    ws.onmessage = function (e) {
        // e.data contains received JSON-encoded string.
        parsed_data = JSON.parse(e.data);
        output("onmessage: " + e.data);
    };

    ws.onclose = function () {
        output("onclose");
        output("Session to Tecan Robotic service has been shut down.  Close window and restart python service.");
        var mainDiv = document.getElementById("main");
        mainDiv.style.display = "none";
    };

    ws.onerror = function (e) {
        output("onerror");
        console.log(e)
    };

}
