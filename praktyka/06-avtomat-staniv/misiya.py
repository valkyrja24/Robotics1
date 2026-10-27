from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)
time.sleep(0.5)
gyro.reset()

STINA = 15
NYZKYI_ZARYAD = 30
START_ZARYAD = 60
VYTRATA_PATRUL = 3.0
VYTRATA_BAZA = 1.5
ZARYADKA_SHVYD = 25.0

TAIMAUT = {
    "patrul": 25,
    "na_bazu": 25,
    "povorot": 6,
    "zaryadka": 10,
}

stan = "patrul"
vkhid = time.time()
zaryad = START_ZARYAD
pravykh = 0
kut_cil = 0
storona = 1
pislya = "patrul"
ostannii = time.time()


def perekhid(novyi):
    global stan, vkhid
    print(stan, "->", novyi, "  заряд", round(zaryad), "%")
    stan = novyi
    vkhid = time.time()
    if novyi == "povorot":
        gyro.reset()
    if novyi in ("zaryadka", "gotovo"):
        tank.off()


def povernuty(kut, kudy, potim):
    global kut_cil, storona, pislya
    kut_cil, storona, pislya = kut, kudy, potim
    tank.off()
    perekhid("povorot")


print("старт: patrul, заряд", START_ZARYAD, "%")

while stan != "gotovo":
    d = ultra.distance_centimeters
    if d < 3:
        d = 255
    teper = time.time()
    dt = teper - ostannii
    ostannii = teper

    if stan == "patrul":
        tank.on(SpeedPercent(30), SpeedPercent(30))
        zaryad -= VYTRATA_PATRUL * dt
        if zaryad < NYZKYI_ZARYAD:
            povernuty(180, 1, "na_bazu")
        elif d < STINA:
            pravykh += 1
            povernuty(90, 1, "patrul")

    elif stan == "na_bazu":
        tank.on(SpeedPercent(25), SpeedPercent(25))
        zaryad -= VYTRATA_BAZA * dt
        if d < STINA and pravykh == 0:
            perekhid("zaryadka")
        elif d < STINA:
            pravykh -= 1
            povernuty(90, -1, "na_bazu")

    elif stan == "povorot":
        tank.on(SpeedPercent(20 * storona), SpeedPercent(-20 * storona))
        if abs(gyro.angle) >= kut_cil - 3:
            tank.off()
            perekhid(pislya)

    elif stan == "zaryadka":
        zaryad = min(100, zaryad + ZARYADKA_SHVYD * dt)
        if zaryad >= 100:
            perekhid("gotovo")

    if stan in TAIMAUT and teper - vkhid > TAIMAUT[stan]:
        print("таймаут у стані", stan)
        tank.off()
        break

    time.sleep(0.05)

print("кінець: заряд", round(zaryad), "%")
