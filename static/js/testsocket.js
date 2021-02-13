let sock;
sock = new WebSocket('ws://' + "127.0.0.1:8080" + '/ws');


sock.onopen = function(){
    sock.send(JSON.stringify({data: "test"}))
}

// send message from form
