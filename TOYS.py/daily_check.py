import random
import math
import datetime

# --- The Logic Module (Same formula as before) ---
def calculate_dew_point(temp_c, humidity):
    b = 17.62
    c = 243.12
    gamma = (b * temp_c) / (c + temp_c) + math.log(humidity / 100.0)
    dew_point = (c * gamma) / (b - gamma)
    return dew_point

# --- Simulation ---
# Simulate a sensor reading between 20C and 28C
temp = random.uniform(20.0, 28.0)
# Simulate humidity between 40% and 60%
humid = random.uniform(40.0, 60.0)

# Calculate
dp = calculate_dew_point(temp, humid)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- The Logger (Writing to file instead of screen) ---
log_entry = f"{timestamp}, {temp:.2f}, {humid:.2f}, {dp:.2f}\n"

# "a" mode means Append (add to bottom), not Overwrite
with open("environment_log.csv", "a") as file:
    file.write(log_entry)

print("Log entry saved.")