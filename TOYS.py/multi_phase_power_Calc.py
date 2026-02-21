import tkinter as tk
from tkinter import messagebox
import logging
import math

# 1. Compliance Logging Setup
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. Decoupled Configuration
CONFIG = {
    "safety_limits": {
        "1_phase_max_v": 240.0,
        "3_phase_max_v": 415.0,
        "max_amperage": 200.0
    },
    "system": {
        "power_factor": 0.95  # Standard assumed data center PF
    },
    "ui": {
        "title": "Critical Power Dashboard",
        "geometry": "420x380",
        "bg_color": "#ececec"
    }
}

# 3. Logic & Simulation Class
class MockPowerSensors:
    """Handles calculations, phase logic, and enforces safety interlocks."""
    def __init__(self, limits, system_config):
        self.limits = limits
        self.pf = system_config["power_factor"]

    def calculate_watts(self, voltage, current, phase_type):
        # Determine voltage cap based on phase selection
        v_cap = self.limits["3_phase_max_v"] if phase_type == 3 else self.limits["1_phase_max_v"]
        
        # Safety Interlocks
        if voltage > v_cap:
            logging.warning(f"Interlock Triggered: {voltage}V exceeds {phase_type}-phase cap of {v_cap}V.")
            raise ValueError(f"Voltage exceeds {phase_type}-phase safety limit of {v_cap}V.")
        
        if current > self.limits["max_amperage"]:
            logging.warning(f"Interlock Triggered: {current}A exceeds system cap.")
            raise ValueError(f"Current exceeds safety limit of {self.limits['max_amperage']}A.")
        
        # Calculation Logic
        if phase_type == 3:
            watts = voltage * current * math.sqrt(3) * self.pf
        else:
            watts = voltage * current * self.pf
            
        logging.info(f"Load calculated ({phase_type}-Phase): {voltage}V @ {current}A = {watts:.2f}W")
        return watts

# 4. GUI Implementation
class PowerDashboard:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.title(self.config["ui"]["title"])
        self.root.geometry(self.config["ui"]["geometry"])
        self.root.configure(bg=self.config["ui"]["bg_color"])
        
        self.logic = MockPowerSensors(self.config["safety_limits"], self.config["system"])
        
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, bg=self.config["ui"]["bg_color"], padx=20, pady=20)
        frame.pack(expand=True)

        # Phase Toggle (Radio Buttons)
        tk.Label(frame, text="System Phase:", bg=self.config["ui"]["bg_color"], font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        
        self.phase_var = tk.IntVar(value=3) # Default to 3-Phase
        
        tk.Radiobutton(frame, text="1-Phase (Max 240V)", variable=self.phase_var, value=1, bg=self.config["ui"]["bg_color"]).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(frame, text="3-Phase (Max 415V)", variable=self.phase_var, value=3, bg=self.config["ui"]["bg_color"]).grid(row=1, column=1, sticky="w")

        # Voltage Input
        tk.Label(frame, text="Voltage (V):", bg=self.config["ui"]["bg_color"]).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_voltage = tk.Entry(frame)
        self.entry_voltage.grid(row=2, column=1, pady=5)

        # Current Input
        tk.Label(frame, text="Current (A):", bg=self.config["ui"]["bg_color"]).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_current = tk.Entry(frame)
        self.entry_current.grid(row=3, column=1, pady=5)

        # Calculate Button
        calc_btn = tk.Button(frame, text="Calculate Power", command=self.perform_calculation, bg="#0078D7", fg="white", font=("Arial", 10, "bold"))
        calc_btn.grid(row=4, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

        # Output Display
        self.lbl_result = tk.Label(frame, text="Watts (W): --", font=("Arial", 14, "bold"), bg=self.config["ui"]["bg_color"])
        self.lbl_result.grid(row=5, column=0, columnspan=2, pady=10)

    def perform_calculation(self):
        try:
            # Parse inputs
            v_val = float(self.entry_voltage.get())
            a_val = float(self.entry_current.get())
            phase_val = self.phase_var.get()
            
            # Process through the logic class
            watts = self.logic.calculate_watts(v_val, a_val, phase_val)
            
            # Update GUI
            self.lbl_result.config(text=f"Power: {watts:,.2f} W", fg="#228B22") # Forest Green
            
        except ValueError as e:
            # Handle non-numeric input or safety interlock violations
            error_msg = str(e) if "safety limit" in str(e) else "Please enter valid numeric values."
            self.lbl_result.config(text="Power: Interlock Tripped", fg="#D32F2F") # Red
            messagebox.showerror("Validation Error", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerDashboard(root, CONFIG)
    root.mainloop()
    