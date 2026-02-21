import random

class SensorInterface:
    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode

    def get_live_weight(self):
        """
        In the future, this will poll the Modbus register.
        For now, if we are simulating, return a random realistic value
        or None to indicate 'Manual Entry' is needed.
        """
        if self.simulation_mode:
            # Return a mock float for testing visual feedback
            return round(random.uniform(80.0, 190.0), 2) 
        else:
            # Later: return minimal_modbus.read_float(...)
            pass