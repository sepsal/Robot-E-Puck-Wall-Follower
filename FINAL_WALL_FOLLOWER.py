import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
from controller import Robot

# Create an instance of the Robot class
robot = Robot()

ps5_sensor = robot.getDevice("ps5")
ps7_sensor = robot.getDevice("ps7")

ps5_sensor.enable(10)
ps7_sensor.enable(10)

max5 = ps5_sensor.getMinValue()
max7 = ps7_sensor.getMinValue()

# Mendapatkan penampilan motor
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

# Set kecepatan maksimum motor
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

ps5 = ctrl.Antecedent(np.arange(68, 1501, 1), 'ps5')

kecepatan = ctrl.Consequent(np.arange(0, 3, 0.1), 'kecepatan')

ps5['kecil'] = fuzz.trimf(ps5.universe, [68, 68, 200])
ps5['sedang'] = fuzz.trimf(ps5.universe, [100, 300, 1000])
ps5['besar'] = fuzz.trimf(ps5.universe, [900, 1500, 1500])

kecepatan['normal'] = fuzz.trimf(kecepatan.universe, [0, 0, 3])
kecepatan['fast'] = fuzz.trimf(kecepatan.universe, [2, 5, 5])

#Motor Kiri
rule1 = ctrl.Rule(ps5['kecil'], kecepatan['fast'])
rule2 = ctrl.Rule(ps5['sedang'], kecepatan['normal'])
rule3 = ctrl.Rule(ps5['besar'], kecepatan['fast'])

speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
speed_controller = ctrl.ControlSystemSimulation(speed_ctrl)

while robot.step(10) != -1:
    # Get distance sensor values
    ps7_value = ps7_sensor.getValue()
    ps5_value = ps5_sensor.getValue()
    print("PS7:", int(ps7_value), "| PS5:", int(ps5_value))
    
    # Set input values
    speed_controller.input['ps5'] = ps5_value

    # Compute control
    speed_controller.compute()

    # Get output values
    kecepatan_value = speed_controller.output['kecepatan']
    
    print(kecepatan_value)
    
    if ps7_value <= 100 and 200 <= ps5_value <= 550:
        a = 2.5 
        b = 2.5
    elif ps7_value <= 100 and ps5_value < 550:
        a = 2.5 
        b = 2.5 + kecepatan_value
    elif ps7_value <= 100 and ps5_value > 400:
        a = 2.5 + kecepatan_value
        b = 2.5
    elif ps7_value > 100 and ps5_value < 550:
        a = 2.0 + (kecepatan_value*3.0)
        b = 2.0 - (kecepatan_value*3.0)
    elif ps7_value > 100 and ps5_value > 400:
        a = 2.0 + (kecepatan_value*1.5)
        b = 2.0 - (kecepatan_value*1.5)
    left_motor.setVelocity(a)
    right_motor.setVelocity(b)
    print(a)
    print(b)