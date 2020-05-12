import serial, string, time

ser = serial.Serial('\\\\.\\CNCB0', 9600, 8, 'N', 1, timeout=3) 

fs = open('nellcor.txt', 'r') 
count = 0
  
while True: 
    # Get next line from file 
    line = fs.readline() 
  
    # if line is empty 
    # end of file is reached 
    if line.strip() == "":
        continue
    elif not line: 
        break
    count += 1
    print("Line{}: {}".format(count, line.strip())) 
    ser.write(bytes(line, 'ascii'))
    time.sleep(2)
fs.close() 

