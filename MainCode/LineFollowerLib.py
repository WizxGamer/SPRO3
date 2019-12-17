import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

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

def go_straight():

    if left_ir_sensor() > 40 and right_ir_sensor() > 40:
        r_motor = 0
        l_motor = 0

        timeout = timeout - 1
        print ("Timeout {}".format(timeout))
        time.sleep(0.01)

        if timeout <= 0:
            return False
    else:
        if timeout != 5:
            timeout = 5

        if central_ir_sensor() > 50:
            r_motor = 80
            l_motor = 100
        else:
            r_motor = 100
            l_motor = 80

    if right_ir_sensor() > 80 and left_ir_sensor() < 80:
        r_motor = 0
        l_motor = 50

    if left_ir_sensor() > 80 and right_ir_sensor() < 80:
        r_motor = 50
        l_motor = 0

    set_motors(r_motor, l_motor)
    return True


bounce = 0

def turn(direction):
    print ("Middle Sensor: {}, Bounce: {}".format(central_ir_sensor(), bounce))
    if direction == 1:
        while left_ir_sensor() > 40 and right_ir_sensor() > 40:
            r_motor = 50
            l_motor = 50

    if direction == 2:

        if central_ir_sensor() > 40:
            l_motor = -40
            r_motor = 50
            if bounce == 0:
                bounce = 1

        if central_ir_sensor() < 40 and bounce >= 1:
            l_motor = -40
            r_motor = 50
            if bounce == 1:
                bounce = 2

        if central_ir_sensor() > 40 and bounce >= 2:
            set_motors(0, 0)
            bounce = 0
            return False

    if direction == 3:
        if central_ir_sensor() > 40:
            r_motor = -40
            l_motor = 90
            if bounce == 0:
                bounce = 1

        if central_ir_sensor() < 40 and bounce >= 1:
            r_motor = -40
            l_motor = 90
            if bounce == 1:
                bounce = 2

        if central_ir_sensor() > 60 and bounce >= 2:
            r_motor = 0
            l_motor = 0
            bounce = 0
            return False

    set_motors(r_motor, l_motor)
    return True

def cam_function(x, y):
    pass

def metal_sensor_triggered():
    return False
