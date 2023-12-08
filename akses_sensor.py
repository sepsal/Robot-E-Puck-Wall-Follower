from controller import Robot

# inisialisasi robot
robot = Robot()

# inisialisasi sensor proximity
timestep = int(robot.getBasicTimeStep())

proximity5 = robot.getDevice('ps5')
proximity5.enable(timestep)
proximity7 = robot.getDevice('ps7')
proximity7.enable(timestep)

while robot.step(timestep) != -1:
    # membaca nilai sensor
    val_ps5 = proximity5.getValue()
    val_ps7 = proximity7.getValue()
    x1 = proximity5.getMinValue()
    y1 = proximity5.getMaxValue()
    x2 = proximity7.getMinValue()
    y2 = proximity7.getMaxValue()
    # tampilkan nilai sensor di console
    print("Proximity Sensor 5: ", format(val_ps5))
    print("Proximity Sensor 7: ", format(val_ps7))
    print("Max : ", y1)
    print("Min : ", x1)
    print("Max : ", y2)
    print("Min : ", x2)