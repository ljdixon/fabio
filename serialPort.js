const SerialPort = require('serialport')
const Readline = SerialPort.parsers.Readline
const MockBinding = require('@serialport/binding-mock')

SerialPort.Binding = MockBinding

// Create a port and enable the echo and recording.
MockBinding.createPort('/dev/ROBOT', { echo: true })
const port = new SerialPort('/dev/ROBOT')
const parser = new Readline()
port.pipe(parser)
parser.on('data', console.log)
var i;
for (i = 0; i < 10; i++) {
    //port.write('22-Aug-16 15:27:12   ---     ---     ---    SD\n')
}

const waitForData = async () => {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => reject('Write Timeout'), 500);
  
      parser.once('data', (data) => {
        clearTimeout(timeoutId);
        resolve(data);
      });
    });
  };

const writeData = async () => {
  while(true) {
    port.write('22-Aug-16 15:27:12   ---     ---     ---    SD\n')
    const data = await waitForData();
  }
}