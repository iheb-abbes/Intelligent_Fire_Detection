import time
import os
import cv2
from ultralytics import YOLO

class FireDetector:
    def __init__(self, model_path='pc_system/models/fire_smoke'): 
        """
        Module 4.2: Responsible for detecting fire and smoke.
        Spatial filtering added to reduce false positives from walls/background.
        """
        if os.path.exists(model_path):
            self.model = YOLO(model_path)
            print(f"DEBUG: Loaded Multi-Class Model. Labels: {self.model.names}")
        elif os.path.exists(model_path + ".pt"):
            self.model = YOLO(model_path + ".pt")
            print(f"DEBUG: Loaded Multi-Class Model (.pt). Labels: {self.model.names}")
        else:
            self.model = YOLO('yolov8n.pt') 
            print(f"WARNING: {model_path} not found! Using default YOLOv8 labels.")

        self.alert_start_time = None
        self.is_confirmed = False

    def detect(self, frame):
        # 1. Higher confidence (0.50) to filter out weak 'wall' detections
        results = self.model(frame, verbose=False, conf=0.50) 
        
        detections = []
        hazard_found = False
        
        # Get frame dimensions for spatial filtering
        h, w, _ = frame.shape
        frame_area = h * w

        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()
            confidences = r.boxes.conf.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()

            for box, conf, cls in zip(boxes, confidences, classes):
                label = self.model.names[int(cls)]
                
                # Calculate bounding box area ratio
                x1, y1, x2, y2 = box
                box_area = (x2 - x1) * (y2 - y1)
                area_ratio = box_area / frame_area

                # Check for Fire OR Smoke
                if label.lower() in ['fire', 'smoke', 'flame']: 
                    
                    # 2. Size Filter: If 'smoke' covers > 70% of screen, ignore it (likely a wall)
                    if label.lower() == 'smoke' and area_ratio > 0.70:
                        continue 

                    hazard_found = True
                    detections.append({
                        "timestamp": time.time(),
                        "label": label.upper(),
                        "confidence": float(conf),
                        "bbox": box.tolist()
                    })

        # --- 1-Second Verification Logic (Module 4.2) ---
        if hazard_found:
            if self.alert_start_time is None:
                self.alert_start_time = time.time()
            elif time.time() - self.alert_start_time >= 1.0:
                self.is_confirmed = True
        else:
            self.alert_start_time = None
            self.is_confirmed = False

        return detections, self.is_confirmed