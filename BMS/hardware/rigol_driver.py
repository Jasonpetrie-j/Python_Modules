import pyvisa
import time
import json
import os

class PowerMonitor:
    def __init__(self):
        self.inst = None
        self.rm = None
        self.connected = False
        self.config = self._load_config()
        self.address = self.config.get("rigol_ip", "TCPIP0::192.168.1.102::INSTR")
        
    def _load_config(self):
        """Reads configuration parameters from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback defaults ensuring safe BNC parameters
            return {
                "rigol_ip": "TCPIP0::192.168.1.102::INSTR",
                "bnc_attenuation": 10, # Default to 10X probe for safety
                "bnc_impedance": "OMEG" # OMEG = 1M Ohm, FIFTy = 50 Ohm
            }

    def connect(self):
        """Establishes connection using PyVISA"""
        try:
            print(f"Opening Resource Manager...")
            self.rm = pyvisa.ResourceManager('@py') 
            
            print(f"Connecting to {self.address}...")
            self.inst = self.rm.open_resource(self.address)
            self.inst.timeout = 5000 
            
            idn = self.inst.query("*IDN?")
            print(f"SUCCESS: Connected to {idn.strip()}")
            self.connected = True
            return True
            
        except Exception as e:
            print(f"CONNECTION FAILED: {e}")
            self.connected = False
            return False

    def configure_bnc(self, channel=1):
        """
        Configures the physical BNC input.
        Acts as a safety interlock by enforcing impedance and attenuation limits.
        """
        if not self.connected: return
        
        att = self.config.get("bnc_attenuation", 10)
        imp = self.config.get("bnc_impedance", "OMEG")
        
        try:
            print(f"Configuring BNC CH{channel}: {att}X Attenuation, Impedance: {imp}")
            # Set Probe Attenuation Ratio (1, 10, 100, 1000)
            self.inst.write(f":CHAN{channel}:PROB {att}")
            
            # Set Input Impedance (OMEG = 1 MegaOhm, FIFTy = 50 Ohm)
            self.inst.write(f":CHAN{channel}:IMP {imp}")
            
            # Optional: Add a low-pass filter to clean up noisy facility power lines
            self.inst.write(f":CHAN{channel}:BWL 20M") 
        except Exception as e:
            print(f"Error configuring BNC: {e}")

    def enable_source(self):
        """Turns on the internal Function Generator"""
        if not self.connected: return
        
        print("Initializing Generator...")
        try:
            # 60Hz Sine, 3V Amplitude
            self.inst.write(":SOUR1:APPL:SIN 60,3,0,0")
            self.inst.write(":SOUR1:OUTP ON")
            
            # Setup Channel 1 Display
            self.inst.write(":CHAN1:DISP ON")
            self.inst.write(":CHAN1:COUP AC")
            self.inst.write(":AUTOSCALE")
            time.sleep(4) 
        except Exception as e:
            print(f"Error setting up source: {e}")

    def get_readings(self):
        """Returns (Voltage_RMS, Frequency)"""
        if not self.connected: return 0.0, 0.0
        
        try:
            v_rms = float(self.inst.query(":MEAS:ITEM? VRMS,CHAN1"))
            freq = float(self.inst.query(":MEAS:ITEM? FREQ,CHAN1"))
            return v_rms, freq
        except Exception as e:
            return 0.0, 0.0

    def close(self):
        if self.inst: self.inst.close()
        if self.rm: self.rm.close()

if __name__ == "__main__":
    monitor = PowerMonitor()
    if monitor.connect():
        monitor.configure_bnc(channel=1) # Apply BNC settings before autoscaling
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