sensors = [68, 70, 72, 75, 80, 200]  # The 200 is a ghost voltage/bad sensor
setpoint = 74

print("Starting CRAC Monitor...")

for reading in sensors:
    # We want to calculate the difference (Delta)
    delta = setpoint - reading
    
    if reading > 100:
        print(f"ALARM: Sensor Fault! Reading: {reading}")
        continue  # <--- ADD THIS. It forces the loop to skip to the next sensor.
        
    if delta < 0:
        print(f"Cooling Active. Temp is {reading}. Delta: {delta}")
    else:
        print(f"Unit Idle. Temp is {reading}")

print("Cycle Complete")