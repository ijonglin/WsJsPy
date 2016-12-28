/**
 * Created by ijonglin on 12/23/16.
 */

function output(str) {
    var log = document.getElementById("log");
    var escaped = str.replace(/&/, "&amp;").replace(/</, "&lt;").replace(/>/, "&gt;").replace(/"/, "&quot;"); // "
    log.innerHTML = escaped + "<br>" + log.innerHTML;
}

function onSubmit() {
    ws.send("I got here.")
}

function main() {
    // Pass this around as a global.
    ws = WsJsPyMinimalInit();

    ws.onOpen = function () {
        output("onopen");
    };

    ws.onmessage = function (e) {
        // e.data contains received JSON-encoded string.
        parsed_data = JSON.parse(e.data);
        output("onmessage: " + e.data);
    };

    ws.onclose = function () {
        output("onclose");
        var mainDiv = document.getElementById("main");
        mainDiv.style.display = "none";
    };

    ws.onerror = function (e) {
        output("onerror");
        console.log(e)
    };

    ws.init();
}



