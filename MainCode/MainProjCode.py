import threading
import time
from NavLibrary import Navigation
from LineFollowerLib import go_straight, turn, metal_sensor_triggered, cam_function

Progress = 0

def Turning(Axis, Orientation, Route):
    global Progress
    while turn(Route[Progress]):
        time.sleep(0.01)
    Progress = Progress + 1


if __name__ == "__main__":
    nav = Navigation()
    route = [3, 3, 2, 2]

    while True:
        if Progress == 4:
            break
        if nav.getAxis() == 0:
            if nav.getOrientation() == 0:

                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif route[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(1)
                if metal_sensor_triggered():
                    cam_function(nav.getX(), nav.getY())

            elif nav.getOrientation() == 1:

                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif route[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(1)
                pass

            else:
                break
        elif nav.getAxis() == 1:
            if nav.getOrientation() == 0:

                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(0)
                    elif route[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(0)
                pass

            elif nav.getOrientation() == 1:

                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:     # If we just turned right
                        nav.setOrientation(0)
                        nav.setAxis(0)
                    elif route[Progress-1] == 2:   # If we just turned left
                        nav.setOrientation(1)
                        nav.setAxis(0)
                pass

            else:
                break
        else:
            break
        
        time.sleep(0.01)

    ##Turn everything off
    set_motors(0, 0)
    raise Exception("This should absolutely never happen")
