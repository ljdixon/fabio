const SerialPort = require('serialport')
const Readline = SerialPort.parsers.Readline
const MockBinding = require('@serialport/binding-mock')

SerialPort.Binding = MockBinding

// Create a port and enable the echo and recording.
MockBinding.createPort('/dev/ROBOT', { echo: true, record: true })
const port = new SerialPort('/dev/ROBOT')
const parser = new Readline()
port.pipe(parser)
parser.on('data', console.log)
var i;
for (i = 0; i < 10; i++) {
    port.write('22-Aug-16 15:27:12   ---     ---     ---    SD\n')
}
// ROBOT ONLINE