from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)
color = ColorSensor(INPUT_1)

time.sleep(0.5)

BRAKE_ZONE = 40
MIN_SPEED = 5

BACK_5CM_DEGREES = 102

TURN_180_TIME = 2.0

def drive_to_obstacle(stopping_threshold, max_speed=30, smooth=True, extras=True):
    print(f"\n-_-_- СТАРТ. Ціль: зупинка на {stopping_threshold} см, швидкість {max_speed}, плавно: {smooth} -_-_-")

    last_print_time = time.time()
    start_deg = tank.left_motor.position

    while True:
        distance = ultra.distance_centimeters
        color_brightness = color.reflected_light_intensity

        current_time = time.time()
        if current_time - last_print_time >= 1.0:
            print(f"Їду... Відстань: {distance:.1f} см")
            last_print_time = current_time

        if color_brightness < 20:
            tank.off()
            print(f"Стоп. Знайдено лінію (яскравість {color_brightness})")
            break

        if distance <= stopping_threshold:
            distance_trigger = distance
            tank.off()

            time.sleep(0.5)
            fact_distance = ultra.distance_centimeters
            print(f"Тригер на {distance_trigger:.1f} см. Фактична зупинка: {fact_distance:.1f} см")
            print(f"Затримка реакції (інерція): {distance_trigger - fact_distance:.1f} см")
            break

        if smooth:
            speed = (distance - stopping_threshold) * max_speed / BRAKE_ZONE
            if speed < MIN_SPEED: speed = MIN_SPEED
            if speed > max_speed: speed = max_speed
        else:
            speed = max_speed
        tank.on(SpeedPercent(speed), SpeedPercent(speed))
        time.sleep(0.05)

    forward_deg = tank.left_motor.position - start_deg

    if not extras:
        return

    print("-_-_- Здаю назад на 5 см -_-_-")
    before = ultra.distance_centimeters
    tank.on_for_degrees(SpeedPercent(-20), SpeedPercent(-20), BACK_5CM_DEGREES)
    time.sleep(0.5)
    print(f"Відʼїхала на {ultra.distance_centimeters - before:.1f} см")

    print("-_-_- Розворот на 180° -_-_-")
    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), TURN_180_TIME)
    time.sleep(0.5)

    print("-_-_- Їду тим самим шляхом назад -_-_-")
    back_deg = max(0, forward_deg - BACK_5CM_DEGREES)
    if back_deg > 0:
        tank.on_for_degrees(SpeedPercent(max_speed), SpeedPercent(max_speed), back_deg)

def drive_to_obstacle_steps(stopping_threshold=15, speed=30):
    print(f"\n-_-_- d: on_for_seconds кроками, поріг {stopping_threshold} см -_-_-")
    while ultra.distance_centimeters > stopping_threshold:
        tank.on_for_seconds(SpeedPercent(speed), SpeedPercent(speed), 0.1)
    tank.off()
    print(f"Стоп. Відстань: {ultra.distance_centimeters:.1f} см")

def back_up():
    tank.on_for_seconds(SpeedPercent(-30), SpeedPercent(-30), 2)

TEST = "P"

if TEST == "P":
    drive_to_obstacle(stopping_threshold=25, extras=False)
    back_up()
    drive_to_obstacle(stopping_threshold=10)

elif TEST == "c":
    drive_to_obstacle(stopping_threshold=30, extras=False)
    back_up()
    drive_to_obstacle(stopping_threshold=5, extras=False)

elif TEST == "d":
    drive_to_obstacle_steps(stopping_threshold=15)

elif TEST == "ef":
    drive_to_obstacle(stopping_threshold=15, max_speed=30, smooth=False, extras=False)
    back_up()
    back_up()
    drive_to_obstacle(stopping_threshold=15, max_speed=60, smooth=False, extras=False)
