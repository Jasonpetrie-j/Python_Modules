import time
import logging
import os
import json

class Watchdog:
    def __init__(self):
        self.active_alarms = []
        self._setup_logger()
        self.limits = self._load_config()

    def _load_config(self):
        """Loads safety limits from config.json"""
        path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return data.get("safety_limits", {})
        except:
            return {"max_humidity_rh": 85, "min_voltage_v": 2.0}

    def _setup_logger(self):
        """Creates a CSV-style log file"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            filename=os.path.join(log_dir, 'incident_log.txt'),
            level=logging.WARNING,
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def check_system(self, telemetry):
        """
        Analyzes data and returns 'Overrides' if safety is at risk.
        telemetry: dict containing voltage, temp, rh, load, fan_speed
        """
        overrides = {}
        self.active_alarms = []

        # 1. CHECK HUMIDITY (Dew Point Risk)
        limit_rh = self.limits.get("max_humidity_rh", 85)
        if telemetry['rh'] > limit_rh:
            msg = f"HIGH HUMIDITY DETECTED: {telemetry['rh']}% (Limit: {limit_rh}%)"
            self.active_alarms.append(msg)
            
            # INTERLOCK ACTION: Force Fan Speed Lower to reduce cooling
            if telemetry['fan_speed'] > 20:
                overrides['cooling'] = 20 # Force fan to 20%
                logging.warning(f"{msg} -> INTERLOCK ACTIVATED: Lowering Fan to 20%")

        # 2. CHECK VOLTAGE (UPS Battery Risk)
        min_volts = self.limits.get("min_voltage_v", 2.0)
        if telemetry['voltage'] < min_volts:
            msg = f"BROWNOUT DETECTED: {telemetry['voltage']}V (Limit: {min_volts}V)"
            self.active_alarms.append(msg)
            
            # INTERLOCK ACTION: Shed Load (Turn off servers)
            if telemetry['load'] > 0:
                overrides['load'] = 0 # Kill server load
                logging.warning(f"{msg} -> INTERLOCK ACTIVATED: Shedding Load to 0%")

        return overrides, self.active_alarms