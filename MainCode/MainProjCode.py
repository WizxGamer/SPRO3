import threading
import time
from NavLibrary import Navigation
from LineFollowerLib import go_straight, turn, metal_sensor_triggered, cam_function, set_motors
from flask import Flask, render_template, request, redirect, url_for
import threading
import os
import shutil

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])  ## This is the firs page you see when going to the url
def FrontPage():
    if request.method == 'POST':
        WebComm[0] = 1

        return redirect(url_for("RunPage"))  ## If something gets posted on this page, redirect to RunPage()

    return render_template("FrontPage.html")  ## When page is just opened show FrontPage.html


@app.route("/Run", methods=["POST", "GET"])
def RunPage():
    if request.method == 'POST':
        WebComm[0] = 0
        counter = 0
        while counter <= 100:
            try:
                os.remove("/home/pi/static/L{}.jpg".format(counter))
            except:
                pass
            try:
                os.remove("/home/pi/static/R{}.jpg".format(counter))
            except:
                pass
            counter = counter + 1
        return redirect(url_for("ReportPage"))  ## If something gets posted to this page, redirect to ReportPage()

    return render_template("RunPage.html")  ## When page is just opened show RunPage.html


@app.route("/Report", methods=["POST", "GET"])
def ReportPage():
    if request.method == 'POST':
        WebComm[0] = 1
        return redirect(url_for("RunPage"))  ## You get it by now
    return render_template("ReportPage.html")

def HostWeb():
    global app
    app.run(host="0.0.0.0", port=1337, debug=False)  ## hosts script on own ip on port 1337, with debugging on for console


def Filemover(Location):
    dest = "/home/pi/static"
    print ("Starting file mover")
    while(True):
        files = os.listdir(Location)
        for file in files:
            print("Found and moved file")
            time.sleep(3)
            shutil.move(Location + "/" + file, dest)
        time.sleep(0.1)


Progress = 0
WebComm = [0, 0, 0]

def Turning(Axis, Orientation, Route):
    global Progress
    while turn(Route[Progress]):
        time.sleep(0.01)
    Progress = Progress + 1


if __name__ == "__main__":
    global WebComm
    nav = Navigation()
    route = [2, 2, 3, 3, 3, 3, 2, 2, 2, 2]
    mover2 = threading.Thread(target=Filemover, args=("/run/user/1000/gvfs/smb-share:server=rightcam.local,share=homes/RightCam",))
    mover2.start()
    mover1 = threading.Thread(target=Filemover, args=("/run/user/1000/gvfs/smb-share:server=leftcam.local,share=homes/LeftCam",))
    mover1.start()

    print ("moving files")
    web = threading.Thread(target=HostWeb)
    web.start()
    print ("Hosting web")
    while True:
        #print ("X: {}, Y: {}".format(nav.getX(),nav.getY()))
        if WebComm[0] == 0:
            time.sleep(0.01)
            set_motors(0, 0)
        elif nav.getAxis() == 0:
            if nav.getOrientation() == 0:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        print "change to north"
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif route[Progress-1] == 2:     # If we just turned left
                        print "change to south"
                        nav.setOrientation(0)
                        nav.setAxis(1)
                if metal_sensor_triggered():
                    nav.setCoordinates(nav.getX()+1, nav.getY())
                    cam_function(nav.getX(), nav.getY())

            elif nav.getOrientation() == 1:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        print "change to north"
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif route[Progress-1] == 2:     # If we just turned left
                        print "change to south"
                        nav.setOrientation(0)
                        nav.setAxis(1)
                if metal_sensor_triggered():
                    nav.setCoordinates(nav.getX()-1, nav.getY())
                    cam_function(nav.getX(), nav.getY())

            else:
                break
        elif nav.getAxis() == 1:
            if nav.getOrientation() == 0:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        print "change to west"
                        nav.setOrientation(1)
                        nav.setAxis(0)
                    elif route[Progress-1] == 2:     # If we just turned left
                        print "change to east"
                        nav.setOrientation(0)
                        nav.setAxis(0)
                if metal_sensor_triggered():
                    nav.setCoordinates( nav.getX(), nav.getY()+1)
                    cam_function(nav.getX(), nav.getY())

            elif nav.getOrientation() == 1:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:     # If we just turned right
                        print "change to west"
                        nav.setOrientation(0)
                        nav.setAxis(0)
                    elif route[Progress-1] == 2:   # If we just turned left
                        print "change to east"
                        nav.setOrientation(1)
                        nav.setAxis(0)
                if metal_sensor_triggered():
                    nav.setCoordinates( nav.getX(), nav.getY()-1)
                    cam_function(nav.getX(), nav.getY())

            else:
                break
        else:
            break
        
        time.sleep(0.01)

    ##Turn everything off
    set_motors(0, 0)
    mover.stop()
    web.stop()
    raise Exception("This should absolutely never happen")
