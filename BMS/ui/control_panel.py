import tkinter as tk
from tkinter import messagebox
import socket
import threading
import time

PI_IP = '192.168.10.5'
PI_PORT = 5025

class FullLabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Controls: PSU + DMM")
        self.root.geometry("500x400")
        
        # --- Connection ---
        self.sock = None
        self.connect_socket()

        # --- PSU SECTION ---
        frame_psu = tk.LabelFrame(root, text="Power Supply (Actuator)", padx=10, pady=10, fg="blue")
        frame_psu.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_psu, text="Set Voltage:").pack(side="left")
        self.volt_entry = tk.Entry(frame_psu, width=10)
        self.volt_entry.insert(0, "5.0")
        self.volt_entry.pack(side="left", padx=5)
        
        tk.Button(frame_psu, text="SET", command=self.set_voltage).pack(side="left")
        
        self.btn_out = tk.Button(frame_psu, text="OUTPUT ON", bg="green", fg="white", command=self.toggle_output)
        self.btn_out.pack(side="right", padx=10)
        self.output_state = False

        # --- DMM SECTION ---
        frame_dmm = tk.LabelFrame(root, text="Multimeter (Sensor)", padx=10, pady=10, fg="green")
        frame_dmm.pack(fill="x", padx=10, pady=20)
        
        self.lbl_readout = tk.Label(frame_dmm, text="0.000 V", font=("Consolas", 24, "bold"), fg="black", bg="#e0e0e0", width=10)
        self.lbl_readout.pack()
        
        tk.Button(frame_dmm, text="POLL SENSOR", command=self.read_dmm).pack(pady=5)

    def connect_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((PI_IP, PI_PORT))
        except Exception as e:
            messagebox.showerror("Error", f"Connection Failed: {e}")

    def send(self, cmd):
        try:
            self.sock.sendall(cmd.encode('utf-8'))
            return self.sock.recv(1024).decode('utf-8')
        except:
            pass

    def set_voltage(self):
        val = self.volt_entry.get()
        self.send(f"PSU:VOLT {val}") # Note the prefix!

    def toggle_output(self):
        if not self.output_state:
            self.send("PSU:OUTP ON")
            self.btn_out.config(text="OUTPUT OFF", bg="red")
            self.output_state = True
        else:
            self.send("PSU:OUTP OFF")
            self.btn_out.config(text="OUTPUT ON", bg="green")
            self.output_state = False

    def read_dmm(self):
        # Ask Pi to query DMM
        val = self.send("DMM:READ?")
        # Update UI
        self.lbl_readout.config(text=f"{float(val):.3f} V")
        # Recursively call this function every 500ms for "Live" view
        self.root.after(500, self.read_dmm)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullLabGUI(root)
    root.mainloop()