import tkinter as tk
from tkinter import messagebox
import math
import json
import datetime

class AdvancedLoadCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Center Controls: Motor & Neutral Diagnostic")
        
        # UI Setup
        tk.Label(root, text="Circuit Rating (A):").grid(row=0, column=0)
        self.ent_rating = tk.Entry(root); self.ent_rating.insert(0, "30"); self.ent_rating.grid(row=0, column=1)

        tk.Label(root, text="L1 Amps:").grid(row=1, column=0)
        self.ent_l1 = tk.Entry(root); self.ent_l1.grid(row=1, column=1)
        
        tk.Label(root, text="L2 Amps:").grid(row=2, column=0)
        self.ent_l2 = tk.Entry(root); self.ent_l2.grid(row=2, column=1)
        
        tk.Label(root, text="L3 Amps:").grid(row=3, column=0)
        self.ent_l3 = tk.Entry(root); self.ent_l3.grid(row=3, column=1)

        self.btn_calc = tk.Button(root, text="Run Engineering Diagnostic", command=self.calculate)
        self.btn_calc.grid(row=4, column=0, columnspan=2, pady=10)

        # Output Display
        self.txt_display = tk.Text(root, height=10, width=45, state='disabled', bg="#f0f0f0")
        self.txt_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def calculate(self):
        try:
            r = float(self.ent_rating.get())
            a, b, c = float(self.ent_l1.get()), float(self.ent_l2.get()), float(self.ent_l3.get())
            
            # 1. Estimated Neutral Current (Vector Math)
            # Formula: sqrt(a^2 + b^2 + c^2 - (ab + bc + ca))
            neutral_current = math.sqrt(a**2 + b**2 + c**2 - (a*b + b*c + a*c))
            
            # 2. Imbalance %
            avg = (a + b + c) / 3
            imbalance = (max(abs(a-avg), abs(b-avg), abs(c-avg)) / avg) * 100 if avg > 0 else 0
            
            # 3. Estimated Temp Rise % (Based on NEMA MG-1)
            # Heat increases significantly even with small unbalance
            temp_increase = 2 * (imbalance ** 2)

            self.update_display(a, b, c, neutral_current, imbalance, temp_increase, r)
            
        except Exception as e:
            messagebox.showerror("Error", "Invalid inputs. Ensure all phases have values.")

    def inject_mock_failure(self):
        # Simulating a blown fuse on L3
        self.ent_l1.delete(0, tk.END); self.ent_l1.insert(0, "15.42")
        self.ent_l2.delete(0, tk.END); self.ent_l2.insert(0, "14.98")
        self.ent_l3.delete(0, tk.END); self.ent_l3.insert(0, "0.00")
        self.calculate()
        messagebox.showwarning("Simulation", "MOCK FAILURE: L3 Phase Loss Detected.")
    
    def update_display(self, a, b, c, neutral, imb, temp, rating):
        self.txt_display.config(state='normal')
        self.txt_display.delete('1.0', tk.END)
        
        report = [
            f"--- DIAGNOSTIC REPORT ---",
            f"Neutral Current: {neutral:.2f} A",
            f"Phase Imbalance: {imb:.1f}%",
            f"Est. Temp Increase: {temp:.1f}%",
            f"NEC 80% Capacity: {'OK' if max(a,b,c) <= rating*0.8 else 'OVERLOAD'}",
            f"-------------------------"
        ]
        
        if imb > 10:
            report.append("CRITICAL: High neutral current/heat risk!")
        elif temp > 15:
            report.append("WARNING: Motor insulation life shortening.")
            
        self.txt_display.insert(tk.END, "\n".join(report))
        self.txt_display.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    AdvancedLoadCalculator(root)
    root.mainloop()