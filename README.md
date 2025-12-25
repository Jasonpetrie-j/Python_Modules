# Python Modules for Critical Infrastructure

**Author:** Jason
**Role:** Maintenance Technician III / Aspiring AWS EOT
**Location:** Reno, NV

## Project Overview
This repository contains Python scripts developed to simulate and troubleshoot Data Center operations. These tools demonstrate my ability to translate facility concepts (Cooling, Logic, BMS) into code.

## Modules

### 1. Environment Monitor (`environment.py`)
* **Purpose:** Calculates Dew Point using the Magnus Formula to detect condensation risks.
* **Logic:** Inputs Temp/Humidity -> Returns Dew Point.
* **Safety:** Triggers a "CONDENSATION RISK" alarm if the approach is < 3°C.

### 2. CRAC Unit Troubleshooter (`troubleshoot.py`)
* **Purpose:** Simulates a sensor loop for a cooling unit.
* **Logic:** Scans 6 sensors, identifies faults, and commands cooling based on Delta-T.
* **Feature:** Includes error handling for "Ghost Voltage" (Bad Data).

### 3. Startup Sequence (`startup.py`)
* **Purpose:** Basic verification script to confirm Python runtime is operational.