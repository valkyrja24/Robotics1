from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)

time.sleep(0.5)

tank.on(SpeedPercent(30), SpeedPercent(30))

while color.reflected_light_intensity > 20:
    pass

tank.off()
print("Стоп. Темна лінія. Яскравість: ", color.reflected_light_intensity)
