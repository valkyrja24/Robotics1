from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
gps = GPSSensor(INPUT_4)
time.sleep(0.5)

PORIH = 50
BAZA = 20
Kp = 1.5


def obmezhyty(v):
    return max(-100, min(100, v))


pochatok = time.time()
while time.time() - pochatok < 120 and gps.y < 85:
    v = color.reflected_light_intensity
    e = PORIH - v
    korekciya = Kp * e
    tank.on(SpeedPercent(obmezhyty(BAZA - korekciya)),
            SpeedPercent(obmezhyty(BAZA + korekciya)))

tank.off()
print("Kp = %.2f, час до кінця траси: %.1f с" % (Kp, time.time() - pochatok))
