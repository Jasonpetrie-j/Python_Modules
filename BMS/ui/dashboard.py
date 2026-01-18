import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, root, on_shutdown_callback):
        self.root = root
        self.root.title("AWS Critical Facilities - BMS Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b") # Dark Mode background
        
        self.shutdown_callback = on_shutdown_callback

        # STYLES
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#2b2b2b", foreground="white", font=("Arial", 10))
        style.configure("TFrame", background="#2b2b2b")
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#FFA500") # Amazon Orange

        # --- HEADER ---
        header_frame = ttk.Frame(root, padding=10)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="CRITICAL INFRASTRUCTURE MONITORING", style="Header.TLabel").pack()

        # --- MAIN CONTENT GRID ---
        content = ttk.Frame(root, padding=20)
        content.pack(fill="both", expand=True)

        # === SECTION 1: HARDWARE (The Rigol Data) ===
        power_frame = ttk.LabelFrame(content, text=" UTILITY POWER (RIGOL HIL) ", padding=10)
        power_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.lbl_voltage = self._create_metric(power_frame, "Voltage (Vrms):", "0.00 V")
        self.lbl_freq = self._create_metric(power_frame, "Frequency (Hz):", "0.00 Hz")
        self.lbl_status = tk.Label(power_frame, text="WAITING", bg="gray", fg="black", font=("Arial", 12, "bold"), width=15)
        self.lbl_status.pack(pady=10)

        # === SECTION 2: ENVIRONMENT (The Simulation) ===
        env_frame = ttk.LabelFrame(content, text=" SERVER HALL (SIMULATION) ", padding=10)
        env_frame.grid(row=0, column=1, padx=10, sticky="nsew")

        self.lbl_temp = self._create_metric(env_frame, "Zone Temp:", "-- °F")
        self.lbl_humidity = self._create_metric(env_frame, "Humidity:", "-- %")
        self.lbl_dewpoint = self._create_metric(env_frame, "Dew Point:", "-- °F")

        # ... (Inside __init__, inside the control_frame section) ...
        
        # === SECTION 3: CONTROLS ===
        control_frame = ttk.LabelFrame(root, text=" CONTROL ROOM ", padding=20)
        control_frame.pack(fill="x", padx=20, pady=10)

        # [NEW] Auto Mode Toggle
        self.var_auto = tk.BooleanVar(value=False)
        self.chk_auto = tk.Checkbutton(control_frame, text="ENABLE PID AUTOPILOT", 
                                       variable=self.var_auto, 
                                       bg="#2b2b2b", fg="#00FF00", selectcolor="#444",
                                       font=("Arial", 10, "bold"))
        self.chk_auto.pack(anchor="w", pady=(0, 10))

        # CRAC Fan Speed Slider
        # ... (Rest of code is same) ...

        # CRAC Fan Speed Slider
        ttk.Label(control_frame, text="CRAC Fan Speed (%)").pack(anchor="w")
        self.slider_fan = tk.Scale(control_frame, from_=0, to=100, orient="horizontal", bg="#2b2b2b", fg="white", highlightthickness=0)
        self.slider_fan.set(50) # Start at 50%
        self.slider_fan.pack(fill="x", pady=5)

        # Server Load Slider
        ttk.Label(control_frame, text="Server IT Load (%)").pack(anchor="w")
        self.slider_load = tk.Scale(control_frame, from_=0, to=100, orient="horizontal", bg="#2b2b2b", fg="white", highlightthickness=0)
        self.slider_load.set(80) # Start high
        self.slider_load.pack(fill="x", pady=5)
        
        # Shutdown Button
        btn_exit = tk.Button(root, text="EMERGENCY SHUTDOWN", bg="red", fg="white", font=("Arial", 10, "bold"), command=self.shutdown_callback)
        btn_exit.pack(pady=10)

    def _create_metric(self, parent, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        ttk.Label(frame, text=label_text).pack(side="left")
        value_label = ttk.Label(frame, text=default_value, font=("Consolas", 14, "bold"), foreground="#00FF00") # Matrix Green
        value_label.pack(side="right")
        return value_label

    def update_ui(self, data):
        """Called by Main Loop to update values"""
        # Hardware
        self.lbl_voltage.config(text=f"{data['voltage']:.2f} V")
        self.lbl_freq.config(text=f"{data['freq']:.2f} Hz")
        
        # Color Logic for Status
        if data['status'] == "NORMAL":
            self.lbl_status.config(text="NORMAL", bg="#00FF00", fg="black")
        else:
            self.lbl_status.config(text="BROWNOUT", bg="red", fg="white")

        # Simulation
        self.lbl_temp.config(text=f"{data['temp']:.1f} °F")
        self.lbl_humidity.config(text=f"{data['rh']:.1f} %")
        self.lbl_dewpoint.config(text=f"{data['dp']:.1f} °F")
        
        # Safety Colors
        self.lbl_temp.config(foreground="red" if data['temp'] > 85 else "#00FF00")

    def get_slider_values(self):
        return {
            "cooling": self.slider_fan.get(),
            "load": self.slider_load.get()
        }
    def get_auto_mode(self):
        return self.var_auto.get()