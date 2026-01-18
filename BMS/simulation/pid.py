class PIDController:
    def __init__(self, kp=5.0, ki=0.1, kd=0.05, setpoint=75.0):
        self.kp = kp  # Proportional Gain
        self.ki = ki  # Integral Gain
        self.kd = kd  # Derivative Gain
        self.setpoint = setpoint
        
        self._integral = 0.0
        self._last_error = 0.0

    def update(self, current_value, dt_seconds):
        """
        Calculates the new Fan Speed (0-100%) to hit the Setpoint.
        """
        # 1. Calculate Error (Difference between Goal and Reality)
        error = current_value - self.setpoint
        
        # 2. Proportional Term (The "Muscle")
        p_term = self.kp * error
        
        # 3. Integral Term (The "Fine Tuning")
        # Accumulates error over time to fix small steady-state gaps
        self._integral += error * dt_seconds
        # CLAMP INTEGRAL (Anti-Windup) to prevent runway math
        self._integral = max(-20, min(20, self._integral))
        i_term = self.ki * self._integral
        
        # 4. Derivative Term (The "Brake")
        # Predicts future error based on rate of change
        derivative = (error - self._last_error) / dt_seconds
        d_term = self.kd * derivative
        
        # 5. Combine Output
        output = p_term + i_term + d_term
        
        # Save state for next tick
        self._last_error = error
        
        # 6. Clamp Output to physical limits (Fan can't go < 0% or > 100%)
        return max(0.0, min(100.0, output))