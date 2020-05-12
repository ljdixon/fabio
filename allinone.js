const WebSocket = require('ws');

const spawn = require('child_process').spawn;
py = spawn('python', ['allinone.py']);

const wss = new WebSocket.Server({ port: 8080 });

py.stdout.on('data', function(data){
    //console.log(data.toString());
    wss.clients.forEach(function(wssclient) {
        wssclient.send(data.toString());
    });
});