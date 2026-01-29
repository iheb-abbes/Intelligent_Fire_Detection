import csv
import os
from datetime import datetime

class LoggingModule:
    def __init__(self, log_file='pc_system/logs/detections.csv'):
        self.log_file = log_file
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Initialize CSV file with headers if it's new
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Event', 'Confidence', 'BoundingBox'])

    def log_event(self, detections):
        """
        Logs detection events and their related metadata.
        [cite: 67]
        """
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for det in detections:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Fire Detected",
                    f"{det['confidence']:.2f}",
                    det['bbox']
                ])