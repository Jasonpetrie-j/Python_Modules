import csv, json, os, sys
from datetime import datetime

class CO2Model:
    def __init__(self, config_filename='config.json'):
        if getattr(sys, 'frozen', False):
            self.app_root = os.path.dirname(sys.executable)
        else:
            self.app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.load_config(os.path.join(self.app_root, config_filename))

    def load_config(self, path):
        with open(path, 'r') as f: self.config = json.load(f)

    def get_log_filepath(self, tech_name):
        clean_name = "".join(x for x in tech_name if x.isalnum())
        log_dir = os.path.join(self.app_root, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f"Log_{clean_name}.csv")

    def ensure_log_file(self, tech_name):
        filepath = self.get_log_filepath(tech_name)
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='') as f:
                csv.writer(f).writerow(["Timestamp", "Tech_Name", "Tank_Type", "Serial_ID", "Gross_Lbs", "Net_Lbs", "Gas_Remaining_%"])
        return filepath

    def calculate_metrics(self, gross, tank_type):
        profile = self.config['tank_profiles'][tank_type]
        
        # 1. Pull physics constants from Config
        tare = profile['tare_weight_lbs']
        max_gross = profile['max_gross_weight_lbs']
        
        # 2. Pull Logic Policy from Config (The Fix)
        # Default to 15 if not found, but prefer the config value
        critical_threshold = self.config.get('settings', {}).get('alarm_threshold', 15)

        # 3. Safety Interlock (Your existing robust logic)
        if gross < 0 or gross > max_gross: 
            raise ValueError(f"Safety Limit Exceeded: {gross} lbs")
        
        net = gross - tare
        percent = (net / (max_gross - tare)) * 100
        
        # 4. Return Decision based on Config
        status = "CRITICAL" if percent < critical_threshold else "NORMAL"
        
        return {
            "net_weight": round(net, 2), 
            "percent": max(0, round(percent, 1)), 
            "status": status
        }

    def save_entry(self, tech, tank, serial, gross, net, percent):
        path = self.ensure_log_file(tech)
        with open(path, 'a', newline='') as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tech, tank, serial, gross, net, percent])
        return path