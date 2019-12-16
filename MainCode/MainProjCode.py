import threading
import time
from NavLibrary import Navigation
from LineFollowerLib import go_straight, turn


if __name__ == "__main__":
    nav = Navigation()
    route = [3, 3, 2, 2, 3, 3, 2, 2]
    Progress = 0

    while True:
        if nav.getAxis() == 0:
            if nav.getOrientation() == 0:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif rout[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(1)
            elif nav.getOrientation() == 1:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(1)
                    elif rout[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(1)
            else:
                break
        elif nav.getAxis() == 1:
            if nav.getOrientation() == 0:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:      # If we just turned right
                        nav.setOrientation(1)
                        nav.setAxis(0)
                    elif rout[Progress-1] == 2:     # If we just turned left
                        nav.setOrientation(0)
                        nav.setAxis(0)
            elif nav.getOrientation() == 1:
                if not go_straight():
                    Turning(nav.getAxis, nav.getOrientation, route)
                    if route[Progress-1] == 3:     # If we just turned right
                        nav.setOrientation(0)
                        nav.setAxis(0)
                    elif route[Progress-1] == 2:   # If we just turned left
                        nav.setOrientation(1)
                        nav.setAxis(0)
            else:
                break
        else:
            break
        
        time.sleep(0.01)

    ##Turn everything off
    raise Exception("This should absolutely never happen")

def Turning(Axis, Orientation, Route):
    while turn(Route[Progress]):
        time.sleep(0.01)
    Progress = Progress + 1