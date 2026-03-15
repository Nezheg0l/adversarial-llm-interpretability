import csv
import os
import time

class ExperimentLogger:
    def __init__(self, filename="results/experiment_log.csv"):
        self.filename = filename
        self._init_file()

    def _init_file(self):
        
        if not os.path.exists(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Attack_Type", "Payload", "Success_Initially", "Patch_Time_Sec", "Success_After_Patch"])

    def log_result(self, attack_type, payload, success_initial, patch_time, success_final):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                attack_type,
                payload,
                success_initial,
                patch_time,
                success_final
            ])
            
    def print_stats(self):
        print(f"📊 Data saved to {self.filename}")
