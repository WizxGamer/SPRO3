class Navigation:
    def __init__(self):
        self.Direction_Axis = 0
        self.Direction_Orientation = 0
        self.Y_Coordinate = 0
        self.X_Coordinate = 0

    def setAxis(self, x):
        if x == 0:
            self.Direction_Axis = 0
        elif x == 1:
            self.Direction_Axis = 1
        else:
            raise Exception("Direction Axis cannot be set to {}".format(self.Direction_Axis))

    def setOrientation(self, x):
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