const http = require('http');
const WebSocket = require('ws');

const SerialPort = require('serialport')
const Readline = SerialPort.parsers.Readline
const port = new SerialPort('COM1', {
  baudRate: 115200
})

const parser = new Readline()
port.pipe(parser)


const server = http.createServer(function(request, response) {
    //console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});

const wss = new WebSocket.Server({ server });

const lineByLine = require('n-readlines');
const liner = new lineByLine('nellcor.txt');

let line;

wss.on('connection', function connection(ws) {
    parser.on('data', function(data) {
        ws.send(data)
    })
    
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });
    while (line = liner.next()) {
        //console.log(line.toString('ascii'));
        var data = line.toString().split(" ");
        if(data[0] != "N-550" && data[0] != "TIME" && data[0] != "") {
            console.log(data[0]);
            var time = data[2];
        }
        ws.send(line.toString('ascii') + "<br />");
    }
    
    //console.log('end of line reached');
});

server.listen(8080);