from datetime import datetime
import os
import shutil
import time

FileLocation = os.path.expanduser("/run/user/1000/gvfs/smb-share:server=piren.local,share=homes/LeftCam")
myFileLocation = os.path.expanduser("/home/pi/static")

os.chdir(FileLocation)
while(True):
    for file in os.listdir("."):
        print("File Found")
        time.sleep(1)
        shutil.move(file, myFileLocation)
        print("File moved and renamed")
    time.sleep(0.1);
