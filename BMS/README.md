# Critical Facilities BMS Simulator (Hardware-in-the-Loop)

## Project Overview
This project is a **Building Management System (BMS)** simulator designed to demonstrate **Critical Infrastructure Automation** concepts. It bridges the gap between software (Python) and physical hardware (Rigol Oscilloscope) to create a **Hardware-in-the-Loop (HIL)** test environment.

It simulates the thermodynamics of a Data Center Server Hall, calculating **ASHRAE compliance metrics** (Dew Point, Humidity) in real-time while monitoring actual utility power via an external oscilloscope.

## Key Features
### 1. Hardware-in-the-Loop (HIL) Monitoring
* **Integration:** Connects to a **Rigol DS1074Z-S Oscilloscope** via TCP/IP (LXI Standard) using PyVISA.
* **Real-time Telemetry:** Continuously polls Channel 1 for RMS Voltage and Frequency (simulating Utility Feed).
* **Brownout Detection:** Triggers an automatic "Load Shedding" sequence if voltage drops below critical thresholds (< 2.0V), simulating a UPS battery save event.

### 2. Physics & Thermodynamics Engine
* **Thermal Inertia:** Simulates heat transfer between Server Load (Heat Source) and CRAC Units (Cooling Source).
* **Psychrometrics:** Calculates **Dew Point** in real-time based on Temperature and Relative Humidity.
* **Safety Interlocks:** Automatically overrides operator controls if the environment approaches the Dew Point to prevent condensation (hardware safety).

### 3. PID Automation (Closed-Loop Control)
* Implements a **Proportional-Integral-Derivative (PID)** controller to replace manual operator input.
* Automatically adjusts CRAC Fan Speed to maintain a precise setpoint (75.0°F) regardless of variable Server Load.
* demonstrates "Auto-Pilot" capability common in industrial SCADA systems.

## Tech Stack
* **Language:** Python 3.10+
* **GUI:** Tkinter (Custom Dashboard with Industrial HMI styling)
* **Hardware Interface:** PyVISA (SCPI Command Set)
* **Logic:** PID Control Loop, State Machine Safety Watchdog

## Hardware Requirements
* **Oscilloscope:** Rigol DS1000Z Series (or any LXI-compliant VISA instrument).
* **Network:** Local LAN connection (Ethernet).

## How to Run
1.  **Configure IP:** Update `config.json` with your instrument's VISA Address.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch Dashboard:**
    ```bash
    python main.py
    ```

## Screenshot
*(Add a screenshot of your dashboard here)*