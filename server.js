const http = require('http');
const WebSocket = require('ws');

const SerialPort = require('serialport')
const Readline = SerialPort.parsers.Readline
const port = new SerialPort('COM1', {
  baudRate: 115200
})

const parser = new Readline()
port.pipe(parser)
parser.on('data', console.log)



const server = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});
const wss = new WebSocket.Server({ server });

const lineByLine = require('n-readlines');
const liner = new lineByLine('nellcor.txt');

let line;
let lineNumber = 0;



wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });
    while (line = liner.next()) {
        console.log('Line ' + lineNumber + ': ' + line.toString('ascii'));
        ws.send(line);
        lineNumber++;
    }
    
    console.log('end of line reached');
});

server.listen(8080);