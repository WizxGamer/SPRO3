import threading
import time

class Navigation:
    def __init__(self):
        self.Direction_Axis = 0
        self.Direction_Orientation = 0
        self.Y_Coordinate = 0
        self.X_Coordinate = 0

    def set_Axis(self, x):
        if x == 0:
            self.Direction_Axis = 0
        elif x == 1:
            self.Direction_Axis = 1
        else:
            raise Exception("Direction Axis cannot be set to {}".format(self.Direction_Axis))

    def set_Orientation(self, x):
        if x == 0:
            self.Direction_Orientation = 0
        elif x == 1:
            self.Direction_Orientation = 1
        else:
            raise Exception("Direction Axis cannot be set to {}".format(self.Direction_Orientation))

    def getAxis(self):
        return self.Direction_Axis

    def getOrientation(self):
        return self.Direction_Orientation

    def setCoordinates(self, x, y):
        self.X_Coordinate = x
        self.Y_Coordinate = y


if __name__ == "__main__":
    nav = Navigation()
    while True:
        if nav.getAxis() == 0:
            if nav.getOrientation() == 0:
                print("north")

            elif nav.getOrientation() == 1:
                print("south")
            
            else:
                break
        elif nav.getAxis() == 1:
            if nav.getOrientation() == 0:
                print("east")

            elif nav.getOrientation() == 1:
                print("west")

            else:
                break
        else:
            break
        inp = input("Inp")
        
        time.sleep(0.01)

    ##Turn everything off
    raise Exception("This should absolutely never happen")