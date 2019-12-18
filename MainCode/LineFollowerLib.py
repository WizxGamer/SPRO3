import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

BaseSpeed = 50
MediumSpeed = 45
SlowSpeed = 20

#region gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

GPIO.setwarnings(False)
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
LeftMotorForwards = GPIO.PWM(4, 1000)
LeftMotorForwards.start(0)

GPIO.setup(14, GPIO.OUT)
LeftMotorBackwards = GPIO.PWM(14, 1000)
LeftMotorBackwards.start(0)

GPIO.setup(15, GPIO.OUT)
RightMotorForwards = GPIO.PWM(15, 1000)
RightMotorForwards.start(0)

GPIO.setup(18, GPIO.OUT)
RightMotorBackwards = GPIO.PWM(18, 1000)
RightMotorBackwards.start(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
#endregion

def central_ir_sensor():
    return (mcp.read_adc(0) - 50) / 8.5

def right_ir_sensor():
    return (mcp.read_adc(1) - 50) / 8.5

def left_ir_sensor():
    return (mcp.read_adc(2) - 50) / 8.5

def sharp_ir_sensor():
    return mcp.read_adc(3)

def set_motors(right=0, left=0):
    if left > 0:
        if left <5.3:
            left = 5.3
        LeftMotorForwards.ChangeDutyCycle(left-5.3)
        LeftMotorBackwards.ChangeDutyCycle(0)
    else:
        left = -left
        if left <5.3:
            left = 5.3
        LeftMotorForwards.ChangeDutyCycle(0)
        LeftMotorBackwards.ChangeDutyCycle(left - 5.3)

    if right > 0:
        RightMotorForwards.ChangeDutyCycle(right)
        RightMotorBackwards.ChangeDutyCycle(0)
    else:
        right = -right
        RightMotorForwards.ChangeDutyCycle(0)
        RightMotorBackwards.ChangeDutyCycle(right)


timeout = 0
l_motor = 0
r_motor = 0

def go_straight():
    global timeout
    global l_motor
    global r_motor

    if left_ir_sensor() > 40 and right_ir_sensor() > 40:
        r_motor = 0
        l_motor = 0

        timeout = timeout - 1

        if timeout <= 0:
            print "Junction"
            return False
    else:
        if timeout != 3:
            timeout = 3

        if central_ir_sensor() > 50:
            r_motor = MediumSpeed
            l_motor = BaseSpeed
        else:
            r_motor = BaseSpeed
            l_motor = MediumSpeed

        if central_ir_sensor() > 80:
            #print ("aggTurn {}".format(central_ir_sensor()))
            r_motor = SlowSpeed
            l_motor = BaseSpeed
        elif central_ir_sensor() < 20:
            #print ("aggTurn {}".format(central_ir_sensor()))
            r_motor = BaseSpeed
            l_motor = SlowSpeed

    #print ("Middle Sensor: {}, Left: {} Right: {}".format(central_ir_sensor(), l_motor, r_motor))
    set_motors(r_motor, l_motor)
    return True


bounce = 0


def turn(direction):
    global bounce
    global r_motor
    global l_motor

    #print ("Middle Sensor: {}, Bounce: {}".format(central_ir_sensor(), bounce))
    if direction == 1:
        while left_ir_sensor() > 40 and right_ir_sensor() > 40:
            r_motor = SlowSpeed
            l_motor = SlowSpeed

    if direction == 2:
        l_motor = -SlowSpeed
        r_motor = BaseSpeed

        if central_ir_sensor() > 50:
            if bounce == 0:
                bounce = 1

        if central_ir_sensor() < 60 and bounce >= 1:
            if bounce == 1:
                bounce = 2

        if central_ir_sensor() > 90 and bounce >= 2:
            set_motors(0, 0)
            bounce = 0
            return False

    if direction == 3:

        r_motor = -SlowSpeed
        l_motor = BaseSpeed

        if central_ir_sensor() > 50:
            if bounce == 0:
                bounce = 1

        if central_ir_sensor() < 60 and bounce >= 1:
            if bounce == 1:
                bounce = 2

        if central_ir_sensor() > 90 and bounce >= 2:
            set_motors(0, 0)
            bounce = 0
            return False

    set_motors(r_motor, l_motor)
    return True

def cam_function(x, y):
    set_motors(0, 0)
    GPIO.output(22,1)
    GPIO.output(27,1)
    time.sleep(2)
    GPIO.output(22, 0)
    GPIO.output(27, 0)


bounce2 = 1

def metal_sensor_triggered():
    global bounce2
    if GPIO.input(17) == 0 and bounce2 == 1:
        bounce2 = 0
        return True
    elif GPIO.input(17) == 1 and bounce2 == 0:
        bounce2 = 1
    return False
