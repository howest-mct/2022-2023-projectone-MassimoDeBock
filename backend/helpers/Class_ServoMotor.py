from RPi import GPIO


class ServoMotor:

    def __init__(self, pin, hz=50):
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, hz)
        self.pwm.start(5)

    def set_angle(self, angle):
        if angle < 0:
            angle = 0
        if angle > 180:
            angle = 180
        temp = angle / 180 * 9
        temp = temp + 3
        self.pwm.ChangeDutyCycle(temp)
        return 0
