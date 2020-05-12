#!/usr/bin/python3

import http.server
import socketserver
import socket
import threading
import sys
import json

import serial, string
from PIL import Image, ImageDraw, ImageFont

# Server konfigurieren:
PORT = 4321
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    print('Starting server...')
    sys.stdout.flush()
# bis python3.5
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
# ende python3.5
# ab python3.6
"""
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
"""
# ende python3.6

# Schnittstelle konfigurieren
ser = serial.Serial('\\\\.\\CNCA0', 9600, 8, 'N', 1, timeout=3) 

# Beginn Programm

start_server()
print("server started")
sys.stdout.flush()
output = " "
sys.stdout.flush()
# Nellcor liefet alle 2 Sekunden eine Zeile, also >2 warten bis Zeile vollständig
while True:
  output = ser.readline() # liest Zeile aus Schnittstelle im Bit-Format
  line = str(output,'ascii') # bit-array in ascii-string umwandeln
  line = line[:-1] # new-line am Zeilenende entfernen (return bleibt)
  if line == '':
    continue
  elif line[0:5] == 'N-550':
#      print(line[0:5]) # Zeile mit Limiten
    continue
  elif line[0:5] == '     ': 
#      print('leere Zeile')
    continue
  elif line[0:4] == 'TIME':
#      print('Tabellen-Titel')
    continue
  else: # Zeile mit Messwerten
#      print(line)
#      print(line[0:9]) # Datum
#     Time:
    time_str = line[10:18] # Zeit
#     SaO2:
    sao2_str = line[21:25] # SaO2
#     Heart-Rate:
    hr_str = line[29:33] # HR
#     Alerts
    if (line[32:33] == '*' or line[24:25] == '*'):
      status = '* check values!'
    elif line[21:24] == '---':
      status = 'check device!'
    elif line[0:1] == '':
      status = 'device off'
    else:
      status = 'values ok'

  data = json.dumps({"time":time_str, "sao2":sao2_str, "hr":hr_str, "status":status})
  print(data)
  sys.stdout.flush()