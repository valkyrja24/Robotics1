from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)

time.sleep(0.5)

tank.on(SpeedPercent(30), SpeedPercent(30))

while ultra.distance_centimeters > 15:
    pass

tank.off()
print("Стоп. Відстань до перешкоди: ", ultra.distance_centimeters, "см")
