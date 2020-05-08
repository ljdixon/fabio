#!/usr/bin/python3

import http.server
import socketserver
import socket
import threading

import serial, string
from PIL import Image, ImageDraw, ImageFont

# Server konfigurieren:
PORT = 4321
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    print('Starting server...')
# bis python3.5
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    thread = threading.Thread(target=httpd.serve_forever);
    thread.start();
# ende python3.5
# ab python3.6
"""
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
"""
# ende python3.6


# Bildfunktionen erstellen     
#fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)

def draw_time(time):
  time_img = Image.new('RGB', (315, 60), color = "black")
  d = ImageDraw.Draw(time_img)
  string= "time: "+time
  d.text((10,10), string, fill= "white")
  time_img.save('time.png')
  return

def draw_sao2(sao2):
  sao2_img = Image.new('RGB', (315, 60), color = "green")
  d = ImageDraw.Draw(sao2_img)
  string= "SaO2: "+sao2
  d.text((10,10), string, fill= "yellow")
  sao2_img.save('sao2.png')

def draw_hr(hr):
  hr_img = Image.new('RGB', (315, 60), color = "yellow")
  d = ImageDraw.Draw(hr_img)
  string= "HR: "+hr
  d.text((10,10), string, fill= "red")
  hr_img.save('hr.png')

def draw_ok(status,backgrd,foregrd):
  ok_img = Image.new('RGB', (315, 60), color = backgrd)
  d = ImageDraw.Draw(ok_img)
  string= status
  d.text((10,10), string, fill= foregrd)
  ok_img.save('ok.png')

# Schnittstelle konfigurieren
ser = serial.Serial('COM1', 9600, 8, 'N', 1, timeout=3) 

# Beginn Programm

start_server()
print("server started")
output = " "
# Nellcor liefet alle 2 Sekunden eine Zeile, also >2 warten bis Zeile vollständig
while True:
  while True:
    output = ser.readline() # liest Zeile aus Schnittstelle im Bit-Format
    line=str(output,'ascii') # bit-array in ascii-string umwandeln
    line=line[:-1] # new-line am Zeilenende entfernen (return bleibt)
    if line[0:5] == 'N-550':
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
      draw_time(time_str)
#     SaO2:
      sao2_str = line[21:25] # SaO2
      draw_sao2(sao2_str)
#     Heart-Rate:
      hr_str = line[29:33] # HR
      draw_hr(hr_str)
#     Alerts
      if (line[32:33] == '*' or line[24:25] == '*'):
        status = '* check values!'
        draw_ok(status,"yellow","red")
      elif line[21:24] == '---':
        status = 'check device!'
        draw_ok(status,"yellow","red")
      elif line[0:1] == '':
        status = 'device off'
        draw_ok(status,"yellow","red")
      else:
        status = 'values ok'
        draw_ok(status,"white","green")
      continue
"""


"""


