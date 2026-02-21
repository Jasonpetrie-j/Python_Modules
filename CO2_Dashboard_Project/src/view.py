import customtkinter as ctk

class CO2View(ctk.CTk):
    def __init__(self, controller):
        super().__init__() # Initialize the parent CTk class
        self.controller = controller
        
        # Setup main frame (assuming you have this setup code)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # ---------------------------------------------------------
        # 1. SMART MAPPING (Your "Critical Infrastructure" Logic)
        # ---------------------------------------------------------
        self.tank_map = {
            "K-Size (75lb Tare)": "K-Size",
            "T-Size (100lb Tare)": "T-Size"
        }

        # ---------------------------------------------------------
        # 2. UI SETUP (Must be inside __init__)
        # ---------------------------------------------------------
        
        # --- Tech Name Input ---
        # (This was previously outside the function causing the error)
        self.entry_tech = ctk.CTkEntry(self.main_frame, placeholder_text="Tech Name / ID", justify="center", width=200)
        self.entry_tech.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # --- Cylinder Selection ---
        ctk.CTkLabel(self.main_frame, text="Select Cylinder Size:", text_color="gray").grid(row=2, column=0, columnspan=2)
        
        # Use the KEYS from your map so the dropdown shows friendly names like "K-Size (75lb Tare)"
        self.opt_tank_type = ctk.CTkOptionMenu(
            self.main_frame, 
            values=list(self.tank_map.keys()) 
        )
        self.opt_tank_type.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        # --- Serial & Weight Inputs ---
        self.entry_serial = ctk.CTkEntry(self.main_frame, placeholder_text="Cylinder Serial #", justify="center", width=200)
        self.entry_serial.grid(row=4, column=0, columnspan=2, pady=10)

        self.entry_weight = ctk.CTkEntry(self.main_frame, placeholder_text="Gross Weight (lbs)", justify="center", width=200)
        self.entry_weight.grid(row=5, column=0, columnspan=2, pady=10)

        # --- Status Bar & Buttons ---
        self.status_bar = ctk.CTkProgressBar(self.main_frame, width=300)
        self.status_bar.grid(row=6, column=0, columnspan=2, pady=25)
        self.status_bar.set(0)
        
        self.lbl_status = ctk.CTkLabel(self.main_frame, text="Status: WAITING FOR INPUT", text_color="gray")
        self.lbl_status.grid(row=7, column=0, columnspan=2, pady=(0, 20))

        ctk.CTkButton(self.main_frame, text="Clear", fg_color="gray", command=self.controller.handle_clear).grid(row=8, column=0, padx=10, pady=20, sticky="e")
        ctk.CTkButton(self.main_frame, text="Analyze & Log", command=self.controller.handle_submit).grid(row=8, column=1, padx=10, pady=20, sticky="w")

    # ---------------------------------------------------------
    # 3. HELPER METHODS (Sibling to __init__, not inside it)
    # ---------------------------------------------------------
    def get_selected_tank_key(self):
        """
        Returns the clean JSON key (e.g., 'K-Size') for the backend.
        This isolates the Controller from the UI's messy text.
        """
        display_text = self.opt_tank_type.get()
        return self.tank_map[display_text]

    def update_status(self, msg, color): 
        self.lbl_status.configure(text=msg, text_color=color)

    def set_progress(self, val, color): 
        self.status_bar.configure(progress_color=color)
        self.status_bar.set(val)