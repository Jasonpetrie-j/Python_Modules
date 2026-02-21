import csv
import random
from datetime import datetime, timedelta

# --- Configuration ---
filename = "mock_bms_data.csv"
records_to_generate = 500  # You can change this to 100 or 1000 for more data
start_time = datetime.now()

# Equipment Lists
units = ["CRAC-01", "CRAC-02", "CRAH-01", "CRAH-02"]
zones = ["Server_Hall_A", "Server_Hall_B", "Batt_Room_1"]

def calculate_dew_point(temp_f, humidity):
    """
    Simple approximation for Dew Point: Td = T - ((100 - RH)/5)
    This ensures the data relationship is realistic for your charts.
    """
    return temp_f - ((100 - humidity) / 5)

print(f"Generating {records_to_generate} rows of mock BMS data...")

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # 1. Write the Header Row
    header = [
        "Timestamp", "Unit_ID", "Zone", 
        "Phase_A_Voltage_V", "Phase_B_Voltage_V", "Phase_C_Voltage_V",
        "Supply_Air_Temp_F", "Return_Air_Temp_F", 
        "Rel_Humidity_Pct", "Dew_Point_F", 
        "Power_Draw_kW", "Status_Code"
    ]
    writer.writerow(header)

    # 2. Generate Data
    for i in range(records_to_generate):
        # Time increments by 15 mins per row
        timestamp = start_time + timedelta(minutes=i*15)
        
        unit = random.choice(units)
        # Map specific units to specific zones for consistency
        if "CRAC" in unit:
            zone = "Server_Hall_A"
        else:
            zone = "Server_Hall_B"

        # Simulating 415V 3-Phase Power (fluctuating slightly)
        phase_a = round(random.uniform(412.0, 418.0), 1)
        phase_b = round(random.uniform(412.0, 418.0), 1)
        phase_c = round(random.uniform(412.0, 418.0), 1)

        # Psychrometrics
        supply_temp = round(random.uniform(64.0, 68.0), 1) # Target ~65F
        return_temp = round(random.uniform(82.0, 88.0), 1) # Target ~85F (Hot Aisle)
        humidity = round(random.uniform(40.0, 60.0), 1)    # 40-60% RH
        
        # Calculate Dew Point derived from the other two variables
        dew_point = round(calculate_dew_point(supply_temp, humidity), 1)

        # Power Draw (Randomized load)
        power_draw = round(random.uniform(15.0, 22.0), 2)

        # Status Code: Mostly 0 (Normal), rarely 1 (Warning) or 2 (Critical)
        # Weights: 0 (90%), 1 (8%), 2 (2%)
        status = random.choices([0, 1, 2], weights=[90, 8, 2])[0]

        # Write the row
        writer.writerow([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            unit,
            zone,
            phase_a,
            phase_b,
            phase_c,
            supply_temp,
            return_temp,
            humidity,
            dew_point,
            power_draw,
            status
        ])

print(f"Success! '{filename}' has been created.")