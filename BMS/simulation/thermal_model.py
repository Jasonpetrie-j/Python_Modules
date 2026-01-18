import math
import random

class ServerHall:
    def __init__(self, start_temp=72.0, start_humidity=45.0):
        # Initial Conditions
        self.temp_f = start_temp
        self.humidity = start_humidity
        self.dew_point_f = 0.0
        
        # Physics Constants (Simplified for simulation)
        self.insulation_factor = 0.05  # How fast heat leaks out/in
        self.heat_mass = 20.0          # Thermal inertia (Higher = slower temp changes)

    def calculate_dew_point(self, T, RH):
        """
        Uses the Magnus formula to calculate Dew Point.
        Crucial for Data Center ASHRAE compliance.
        """
        # Constants for Magnus formula
        a = 17.27
        b = 237.7
        
        # Convert F to C for calculation
        temp_c = (T - 32) * 5/9
        
        # Calculate Alpha
        alpha = ((a * temp_c) / (b + temp_c)) + math.log(RH / 100.0)
        
        # Calculate Dew Point in C
        dp_c = (b * alpha) / (a - alpha)
        
        # Return in F
        return (dp_c * 9/5) + 32

    def update(self, server_load_percent, cooling_percent, dt_seconds=1.0):
        """
        The Physics Heartbeat.
        dt_seconds: Time elapsed since last update
        """
        # 1. HEAT GENERATION (Servers + Ambient Heat)
        # 100% Load generates 5 degrees of heat per second (scaled)
        heat_added = (server_load_percent / 100.0) * 5.0
        
        # 2. COOLING (CRAC Unit)
        # 100% Cooling removes 7 degrees per second
        heat_removed = (cooling_percent / 100.0) * 7.0
        
        # 3. APPLY THERMODYNAMICS
        # Net Change = (Heat In - Heat Out) / Thermal Mass
        temp_change = (heat_added - heat_removed) / self.heat_mass
        
        # Apply change with time factor
        self.temp_f += temp_change * dt_seconds

        # 4. HUMIDITY PHYSICS
        # As Temp drops, Relative Humidity RISES (if moisture content is constant)
        # Simple approx: 1 degree drop = ~2% RH increase
        self.humidity -= (temp_change * 2.0)
        
        # Add "Sensor Noise" (Real sensors never stay perfectly still)
        noise = random.uniform(-0.1, 0.1)
        self.temp_f += noise

        # Clamp values to realistic limits
        self.humidity = max(10, min(99, self.humidity))
        self.temp_f = max(40, min(150, self.temp_f))

        # Recalculate Dew Point
        self.dew_point_f = self.calculate_dew_point(self.temp_f, self.humidity)

    def get_metrics(self):
        return {
            "temp_f": round(self.temp_f, 2),
            "humidity_rh": round(self.humidity, 1),
            "dew_point_f": round(self.dew_point_f, 2)
        }

# --- SELF TEST ---
if __name__ == "__main__":
    hall = ServerHall()
    print("--- SIMULATING 10 SECONDS OF FULL LOAD ---")
    for i in range(10):
        # 100% Load, 50% Cooling
        hall.update(server_load_percent=100, cooling_percent=50) 
        m = hall.get_metrics()
        print(f"Time {i}s: Temp={m['temp_f']}F | RH={m['humidity_rh']}% | DP={m['dew_point_f']}F")