from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)

time.sleep(0.5)

MAX_SPEED = 30
BRAKE_ZONE = 40
MIN_SPEED = 5

def drive_to_obstacle(stopping_threshold):
    print(f"\n-_-_- СТАРТ. Ціль: зупинка на {stopping_threshold} см -_-_-")
    while True:
        distance = ultra.distance_centimeters
        if distance <= stopping_threshold:
            break

        speed = (distance - stopping_threshold) * MAX_SPEED / BRAKE_ZONE
        if speed < MIN_SPEED: speed = MIN_SPEED
        if speed > MAX_SPEED: speed = MAX_SPEED

        tank.on(SpeedPercent(speed), SpeedPercent(speed))
        time.sleep(0.05)

    tank.off()
    time.sleep(0.5)
    print(f"Стоп. Поріг {stopping_threshold} см, фактично {ultra.distance_centimeters:.1f} см")

drive_to_obstacle(25)
tank.on_for_seconds(SpeedPercent(-30), SpeedPercent(-30), 2)
drive_to_obstacle(10)
