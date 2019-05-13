import socket
import threading
import os
import re
import time
import RPi.GPIO as GPIO

lenkungPIN = 13
speedPIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(lenkungPIN, GPIO.OUT)
GPIO.setup(speedPIN, GPIO.OUT)

s = GPIO.PWM(lenkungPIN, 50)
s.start(0)
p = GPIO.PWM(speedPIN, 50) # GPIO 17 als PWM mit 50Hz
p.start(0) # Initialisierung

#5 Links / 7 Geradeaus / 9 Rechts



class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def logInfo(self,info : str):			
		print("["+self.getZeit()+"][INFO] " + info)
	def getZeit(self):
		return str(time.strftime("%H:%M:%S"))
	def getDatum(self):
		return str(time.strftime("%d.%m.%Y"))
	def getZeitstempel(self):
		return str(time.strftime("%d.%m.%Y %H:%M:%S"))
	def run(self):
		while True:
			try:
				c, a = self.sock.accept()
				self.logInfo("Neue Verbindung [" + str(c.getpeername()) + "]...")
				
				while True:
					data = str(c.recv(1024), "utf-8")
					if(not data or len(data)== 0):
						break;
					else:
						#handle client inputs
						data = data.split("#")
						a = float(data[0])
						b = float(data[1])
						p.ChangeDutyCycle(7.0+a*2.0)
						s.ChangeDutyCycle(7.0+b*2.0)
						print(data)
			except Exception as er:
				print("Calculatet Error -start")
				print(er)
				print("Calculatet Error -finish")
				pass

	def __init__(self):
		self.logInfo("Der Server wird gestartet...") 
		ip = ""
		port = 11111
		self.sock.bind((ip, port))
		self.sock.listen(1)
		self.logInfo("Server läuft auf der Ip-Adresse: " + str(os.popen("hostname -I").read().replace("\n","").replace('\r',"")) + "mit dem Port: " + str(port))




server = Server();
server.run()
#cThread = threading.Thread(target=server.run)
#cThread.daemon = True
#cThread.start()

p.stop()
GPIO.cleanup()
