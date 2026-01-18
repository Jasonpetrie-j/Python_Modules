import pyvisa
import time
import json
import os

class PowerMonitor:
    def __init__(self):
        self.inst = None
        self.rm = None
        self.connected = False
        self.address = self._load_address()
        
    def _load_address(self):
        """Reads the VISA Address from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                # Default to the one seen in your screenshot if config fails
                return data.get("rigol_ip", "TCPIP0::192.168.1.102::INSTR")
        except FileNotFoundError:
            return "TCPIP0::192.168.1.102::INSTR"

    def connect(self):
        """Establishes connection using PyVISA"""
        try:
            print(f"Opening Resource Manager...")
            self.rm = pyvisa.ResourceManager('@py') # Use the pure python backend
            
            print(f"Connecting to {self.address}...")
            self.inst = self.rm.open_resource(self.address)
            
            # Set timeout to 5 seconds
            self.inst.timeout = 5000 
            
            # Ask the scope "Who are you?"
            idn = self.inst.query("*IDN?")
            print(f"SUCCESS: Connected to {idn.strip()}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"CONNECTION FAILED: {e}")
            self.connected = False
            return False

    def enable_source(self):
        """Turns on the internal Function Generator"""
        if not self.connected: return
        
        print("Initializing Generator...")
        try:
            # 60Hz Sine, 3V Amplitude
            self.inst.write(":SOUR1:APPL:SIN 60,3,0,0")
            self.inst.write(":SOUR1:OUTP ON")
            
            # Setup Channel 1
            self.inst.write(":CHAN1:DISP ON")
            self.inst.write(":CHAN1:COUP AC")
            self.inst.write(":AUTOSCALE")
            time.sleep(4) # Autoscale takes a moment
        except Exception as e:
            print(f"Error setting up source: {e}")

    def get_readings(self):
        """Returns (Voltage_RMS, Frequency)"""
        if not self.connected: return 0.0, 0.0
        
        try:
            # PyVISA query is simple and blocking
            v_rms = float(self.inst.query(":MEAS:ITEM? VRMS,CHAN1"))
            freq = float(self.inst.query(":MEAS:ITEM? FREQ,CHAN1"))
            return v_rms, freq
        except Exception as e:
            # If query fails, return 0s so GUI doesn't crash
            return 0.0, 0.0

    def close(self):
        if self.inst: self.inst.close()
        if self.rm: self.rm.close()

if __name__ == "__main__":
    monitor = PowerMonitor()
    if monitor.connect():
        monitor.enable_source()
        
        print("\n--- MONITORING (Ctrl+C to stop) ---")
        try:
            while True:
                volts, hz = monitor.get_readings()
                status = "NORMAL" if volts > 2.0 else "BROWNOUT"
                print(f"[{status}] Voltage: {volts:.2f} V | Freq: {hz:.2f} Hz")
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.close()
            print("\nTest Stopped.")