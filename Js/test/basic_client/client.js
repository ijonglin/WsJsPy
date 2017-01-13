/**
 * Created by ijonglin on 12/23/16.
 */

function output(str) {
    var log = document.getElementById("log");
    var escaped = str.replace(/&/, "&amp;").replace(/</, "&lt;").replace(/>/, "&gt;").replace(/"/, "&quot;"); // "
    log.innerHTML = log.innerHTML + (escaped + "<br>");
}

function onSubmit() {
    ws.send("I got here.")
}

function messageImplementation(ws) {
    var that = this;
    that.ws = ws;

    that.testState = "START";

    this.messageHandler = function(rawData) {
        parsedData = JSON.parse(rawData);
        switch(testState) {
            case "START":
                if(parsedData.MessageType == "RAW" && parsedData.MessagePayload == "BOOTSTRAP_RESPONSE") {
                    // Do something and send to next state.
                    output("Received Bootstrap Message from Server");
                    output("Sending Bootstrap Message to Server");
                    that.ws.send(
                        JSON.stringify({
                            MessageType: "RAW",
                            MessagePayload: "TEST_MESSAGE"
                        })
                    );
                    output("Sent Bootstrap Message to Server");
                    output("Now waiting for test message from server.");
                    that.testState = "BOOTSTRAP";
                } else {
                    that.testState = "FAILED";
                }
                break;
            case "BOOTSTRAP":
                if(parsedData.MessageType == "RAW" && parsedData.MessagePayload == "TEST_RESPONSE") {
                    // Do something and send to next state.
                    that.testState = "SUCCESS";
                    output("TEST SUCCEEDED on client side");
                } else {
                    that.testState = "FAILED";
                    output("TEST Failed did NOT receive TEST_REPONSE from Server.");
                }
                break;
            default:
                break;
        }

    };

    return this;
};

function main() {
    // Pass this around as a global.
    ws = WsJsPyMinimalInit();

    ws.onOpen = function () {
        output("onopen");
        ws.send(
            JSON.stringify({
                MessageType: "RAW",
                MessagePayload: "BOOTSTRAP"
            })
        );
    };

    var testImpl = messageImplementation(ws);

    ws.onMessage = function (rawData) {
        // e.data contains received JSON-encoded string.
        output("onmessage: " + rawData);
        testImpl.messageHandler(rawData);
    };

    ws.onClose = function () {
        output("onclose");
        var mainDiv = document.getElementById("main");
        mainDiv.style.display = "none";
    };

    ws.onError = function (e) {
        output("onerror");
        console.log(e)
    };

    ws.init();
    //  send bootstrap message
}



