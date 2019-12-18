import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)
from picamera import PiCamera
import time

#import packages for ZBar and OpenCV
from pyzbar import pyzbar
import cv2

camera = PiCamera()
counter = 0

while True:
    if GPIO.input(18):
        print('Image saved to DIR /home/pi/LeftCam_plain/R{}.jpg'.format(counter))
        camera.resolution = (2332, 1944)
        camera.framerate = 15 
        camera.capture('/home/pi/LeftCam_plain/R{}.jpg'.format(counter))
        
        # --- ZBar and OpenCV --- #
        
        #import previously taken picture
        image = cv2.imread('/home/pi/LeftCam_plain/R{}.jpg'.format(counter))
        #detects barcodes in picture
        barcodes = pyzbar.decode(image)
        
        #loop over the detected barcodes
        for barcode in barcodes:
            #extract the barcode's bounding box and draw it
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            #extract barcode data converted from binary) and barcode type
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            
            #draw barcode data and type on picture
            text = "{} ({})".format(barcodeType, barcodeData)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            
            print("Found - Type: {}, Data: {}".format(barcodeType, barcodeData))
            
        cv2.imwrite('/home/pi/LeftCam/R{}.jpg'.format(counter), image)
        #cv2.imshow("Image", image)
        #cv2.waitKey(0)
        
        counter = counter + 1
        time.sleep(2.1)
    
    time.sleep(0.05)



