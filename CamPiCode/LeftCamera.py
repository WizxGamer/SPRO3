import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)
from picamera import PiCamera
import time


camera = PiCamera()
counter = 0

while True:
    if GPIO.input(18):
        print('IPS Trigger HIGH')
        print('Image captured and saved to DIR /home/pi/RightCam/L{}.jpg'.format(counter))
        camera.resolution = (583, 486)
        camera.framerate = 15 
        camera.capture('/home/pi/RightCam/L{}.jpg'.format(counter))
        counter = counter + 1
        time.sleep(2.1)
        
         


