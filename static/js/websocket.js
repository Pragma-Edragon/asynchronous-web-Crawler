const urlToAttack = document.getElementById("AttackedUrl"),
    button = document.getElementById("startAttack");

let websocket;
try {
    websocket = new WebSocket("ws://" + window.location.host + "/ws")
} catch (err) {
    websocket = new WebSocket("wss://" + window.location.host + "/ws" )
}



function createElem(message, uniqueId) {
    if (document.getElementById("queue" + uniqueId) !== null) {
        // update
        let NewTableMessage = document.createElement("li"),
            NewTableMessageLink = document.createElement("a"),
            NewTable = document.getElementById("tableQueue" + uniqueId);

        NewTableMessageLink.appendChild(document.createTextNode(message))
        NewTableMessageLink.setAttribute("href", message)
        NewTableMessage.appendChild(NewTableMessageLink);
        NewTable.appendChild(NewTableMessage);
        document.getElementById("queue" + uniqueId).appendChild(NewTable);
    } else {
        let NewNode = document.createElement("div"),
        NewTableNode = document.createElement("ul");

        NewTableNode.appendChild(document.createTextNode(message));
        NewNode.setAttribute("id", "queue" + uniqueId);
        NewTableNode.setAttribute("id", "tableQueue" + uniqueId);

        NewNode.appendChild(NewTableNode);
        document.body.appendChild(NewNode);
    }
}


websocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data + typeof data)

    switch (data.type) {
        case "state":
            createElem(data.url, data.id);
            break;
        case "update":
            // need to check if attr exists
            createElem(data.state, data.id);
            break;
        case "error":
            console.error(data.error);
            break;
        default:
            console.error("Unsupported event: ", data);
    }
};

button.onclick = function (event) {
    if (urlToAttack.value !== null) {
        websocket.send(JSON.stringify({url: urlToAttack.value}));
        console.log("Send!");
    } else {
        alert("Link must be set.");
    }
};