from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from apiclient.http import MediaFileUpload
from oauth2client import file, client, tools

import RPi.GPIO as GPIO
import time
import picamera
import serial
import MySQLdb
from Tkinter import *



port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)
cam=picamera.PiCamera()
#camera = picamera.PiCamera()
#logvalfile=open('gpsvaluelog.txt','wb')
#new=open('newgpr.txt','wb')
#logfile=open('gprlog.txt','wb')
#port=serial.Serial("/dev/ttyAMA0",9600,timeout=3.0)
db = MySQLdb.connect("localhost", "root", "root", "women_safety")
curs=db.cursor()
port.flushInput()
port.flushOutput()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(22,GPIO.OUT) #buzzer 
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP) #button for everything
#GPIO.setup(4,GPIO.OUT)

while True:
	
	input_state=GPIO.input(17) #check button for everything
	if input_state==False:
		print ("button pressed")
		GPIO.output(22,GPIO.HIGH) #buzzer buzzing
		#GPIO.output(4,GPIO.HIGH)
		#GPS 
		rcvdfile=port.read(1200)
		pos1=rcvdfile.find("$GPRMC")
		pos2=rcvdfile.find("\n",pos1)
		loc=rcvdfile[pos1:pos2]
		#logfile.write(rcvdfile)
		data=loc.split(',')
		if data[2]=='V' :
			print ("Kashmere Gate (2839.85774N, 07713.9255E)")
		else :
	
			gps_time=float(data[1])
			gps_date=float(data[9])
	
	 		gps_hour=int(gps_time/10000.0)
			gps_min=gps_time%10000.0
			gps_sec=gps_min%10000.0
			#gps_min=int(gps_min.100.0)
			gps_sec=int(gps_sec)
	
	 		gps_dd=int(gps_date/10000.0)
			gps_mm=gps_date%10000.0
			gps_yy=gps_mm%100.0
			gps_mm=int(gps_mm/100.0)
			gps_yy=int(gps_yy)
	
			print ('time=',gps_hour,':',gps_min,':',gps_sec)
			print ('date=',gps_dd,'/',gps_mm,'/',gps_yy)
			
			print ("Latitude =  "+data[3]+data[4])
			print ("Longitude =  "+data[5]+data[6])
			
			#latact=float(data[3])
			#longact=float(data[5])
			print ("\n")
			#new.write(data[8])
			
			#print "\n"
			
			#logvalfile.write("\n"+'time='+str(gps_hour)+':'+str(gps_min)+':'+str(gps_sec)+"\n"+'date='+str(gps_dd)+'/'+str(gps_mm)+'/'+str(gps_yy)+"\n")
			
			#logvalfile.write("\n"+"latitude="+data[3]+data[4]+"\n"+"longitude="+data[5]+data[6]+"\n")

		#GPIO.output(4,GPIO.LOW)

		time.sleep(5)

		GPIO.output(22,GPIO.LOW) #buzzer off
		#GSM
		try: 
		
			cam.capture('im4.jpg')
			cam.capture('im5.jpg')
			
			print ("Calling")
			port.write('ATD 8527950252;\r\n')
			
			time.sleep(30)
			#port.write('ATH')
			#port.write('\x1A \r\n')
			sql = "SELECT number FROM emergency_contact"
                        curs.execute(sql)
                        rows = curs.fetchall()
			i=1
                        for row in rows:
                                number= str(row[0])
				print (number)
				cam.capture('img'+str(i)+'.jpg')
				i=i+1
				port.flushInput()
				port.flushOutput()
                                port.write('AT+CMGS="'+number+'"\r\n')
                                time.sleep(2)
                                port.write('SOS\n HELP! HELP!\n I am being attacked.\n My location is : IGDTUW,Kashmere Gate(2839.85774N, 07713.9255E)\r\n')
                                time.sleep(2)
				port.write('\x1A \r\n')
				print (port.read())
				port.flushInput()
				port.flushOutput()
				time.sleep(30)							

			

		except:

			port.close()

		SCOPES = 'https://www.googleapis.com/auth/drive.file'
		store = file.Storage('storage.json')
		creds = store.get()
		if not creds or creds.invalid:
		    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		    creds = tools.run_flow(flow, store)
		
		FILES = ('img1.jpg', 'img2.jpg','img3.jpg')
		  
		DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
		
		for filename in FILES:
		    metadata = {'title': filename}
		    media = MediaFileUpload(filename,mimetype='image/jpeg')
		    file = DRIVE.files().create(body=metadata,media_body=media,fields='id').execute()
		    print ('File ID: %s' % file.get('id'))
    		
		
		time.sleep(5)
		
		break
		
		port.flushInput()
		
		port.flushOutput()