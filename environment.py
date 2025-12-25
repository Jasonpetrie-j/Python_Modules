import math

def calculate_dew_point(temp_c, humidity):
    """
    Calculates Dew Point using the Magnus formula.
    Standard for HVAC/BMS systems.
    """
    # Constants for the formula (Sonntag90)
    b = 17.62
    c = 243.12
    
    # Math logic (Don't worry about the complexity, math module handles it)
    gamma = (b * temp_c) / (c + temp_c) + math.log(humidity / 100.0)
    dew_point = (c * gamma) / (b - gamma)
    
    return dew_point

# --- Main Interface ---
print("--- Data Center Environment Monitor ---")

try:
    # Get input from the technician (You)
    t_input = float(input("Enter Room Temp (°C): "))
    h_input = float(input("Enter Humidity (%): "))

    # Run the calculation function
    dp = calculate_dew_point(t_input, h_input)

    # Output the result formatted to 2 decimal places
    print(f"Calculated Dew Point: {dp:.2f}°C")

    # Safety Logic: The "Approach"
    approach = t_input - dp
    
    if approach < 3:
        print("🚨 ALARM: CONDENSATION RISK! Approach is < 3°C")
    else:
        print("✅ Status: Safe. Air is dry enough.")

except ValueError:
    print("Error: Please enter valid numbers.")