import RPi.GPIO as GPIO
from threading import Thread
import graycode
import time

class Encoder(object):
    def __init__(self, DAT_PIN, CLK_PIN, Tclock=0.00000025):
        GPIO.setmode(GPIO.BCM) # GPIO set mode to BCM
        self.DAT_PIN = DAT_PIN
        self.CLK_PIN = CLK_PIN
        self.Tclock = Tclock
        # self.Tclock = 0.00000025 # 1/4MHz: max CLK signal frequency for SSI ENX 16 EASY Absolute
        # self.Tclock = 0.000025   # 1/0.04MHz: min CLK signal frequency for SSI ENX 16 EASY Absolute
        # self.Tclock = 0.0000025  # Any custom value between min and max
        # self.Tout = 0.000016     # 16us: min timeout for SSI ENX 16 EASY Absolute
        self.Tout = 0.1          # Any custom tout is ok as long as its bigger than 16us
        self.Bitcount = 12 # number of bits transmitted
        self.pos = 0
        self.prev_pos = 0
        self.rotation = 0
        self.count = 0
        self.average_count = 10 # number of readings to eliminate noise

        # pin setup done here
        try:
            GPIO.setup(self.CLK_PIN, GPIO.OUT)
            GPIO.setup(self.DAT_PIN, GPIO.IN)
            GPIO.output(self.CLK_PIN, GPIO.HIGH) # set the clock pin to high
        except:
            print("ERROR. Unable to setup the configuration requested")

        # wait some time to start
        time.sleep(0.1)

        print("GPIO configuration enabled")

    def clockup(self):
        GPIO.output(self.CLK_PIN, GPIO.HIGH)
        
    def clockdown(self):
        GPIO.output(self.CLK_PIN, GPIO.LOW)

    def _update(self):
        while True:
            pos_array = []
            for collect in range(0, self.average_count):
                if GPIO.input(self.DAT_PIN) == GPIO.HIGH:
                    pos = 0
                    self.clockdown()
                    prev_t = time.time()
                    for bit in range(0, self.Bitcount):
                        while True:
                            if time.time() - prev_t >= self.Tclock*(1+0.01):
                                prev_t = time.time()
                                break
                        self.clockup()
                        while True:
                            if time.time() - prev_t >= self.Tclock*(0.1):
                                prev_t = time.time()
                                break
                        last_bit = GPIO.input(self.DAT_PIN)
                        pos <<= 1
                        pos |= last_bit
                        while True:
                            if time.time() - prev_t >= self.Tclock*(1+0.01):
                                prev_t = time.time()
                                break
                        self.clockdown()
                    while True:
                        if time.time() - prev_t >= self.Tclock*(1):
                            prev_t = time.time()
                            break
                    self.clockup()
                pos_array.append(graycode.gray_code_to_tc(pos))
            self.prev_pos = self.pos
            self.pos = max(set(pos_array), key = pos_array.count)
            if (self.prev_pos > 4080 and self.pos < 25):
                self.rotation += 1
            elif (self.prev_pos < 25 and self.pos > 4080):
                self.rotation -= 1
            if self.rotation >= 0:
                self.count = self.rotation * 4095 + self.pos
            else:
                self.count = (self.rotation+1) * 4095 - (4095 - self.pos)
        
    def start(self):
        self.t = Thread(name="Encoder Thread", target=self._update, daemon=True).start()
        return self
    
    def read_pos(self):
        return self.pos
    
    def read_count(self):
        return self.count

if __name__=="__main__":
    encoder = Encoder(17,27).start()
    try:
        while True:
            print(encoder.read_count())
            while True:
                if GPIO.input(encoder.DAT_PIN) == GPIO.HIGH:
                    break
    except KeyboardInterrupt:
        print("cleaning up GPIO")
        GPIO.cleanup()
