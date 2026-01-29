import cv2
import time
import sys
import os
import tkinter as tk
from pc_system.modules.video_input import get_video_stream, process_frame
from pc_system.modules.detection import FireDetector
from pc_system.modules.logging import LoggingModule
from pc_system.modules.communication import CommunicationModule

# --- UI CLASS FOR REMOTE DEACTIVATION (4.6) ---
class ControlPanel:
    def __init__(self, comm_module):
        self.comm = comm_module
        self.root = tk.Tk()
        self.root.title("Fire System Control")
        self.root.geometry("250x100")
        self.root.attributes("-topmost", True) # Keep window on top
        
        tk.Button(self.root, text="STOP ALARM / RESET", 
                  command=self.stop_alarm, bg="red", fg="white", font=('Helvetica', 10, 'bold')).pack(expand=True, pady=20)

    def stop_alarm(self):
        print("[UI] Manual Deactivation Triggered...")
        self.comm.send_alert("off") # Module 4.6 functionality

    def update(self):
        try:
            self.root.update()
        except:
            pass # Handles case where window is closed manually

def main():
    PI_IP = "127.0.0.1" 
    # YouTube source for testing fire and smoke
    VIDEO_SOURCE = "https://www.youtube.com/watch?v=whlymAuRtzU" 
    
    # Initialize Modules
    detector = FireDetector(model_path='pc_system/models/fire.pt') 
    logger = LoggingModule()                                      
    comm = CommunicationModule(PI_IP)                             
    ui = ControlPanel(comm) # Module 4.6
    
    print(f"DEBUG: Connecting to stream...")
    cap = cv2.VideoCapture(get_video_stream(VIDEO_SOURCE))
    
    alert_sent = False

    print("--- System Running: Monitoring Fire & Smoke ---")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            processed_frame = process_frame(frame)
            detections, is_confirmed = detector.detect(processed_frame)
            
            # --- Alert and Logging Logic ---
            if is_confirmed and not alert_sent:
                # Identify if fire or smoke was the trigger for the console message
                trigger_type = detections[0]['label'] if detections else "HAZARD"
                print(f"!!! {trigger_type} CONFIRMED !!! Sending Alert...")
                
                logger.log_event(detections) # Module 4.3
                comm.send_alert("on")        # Module 4.4
                alert_sent = True

            # Reset alert_sent only if screen is completely clear of hazards
            if not detections:
                alert_sent = False

            # --- Visual Overlay (4.6 Interface) ---
            for det in detections:
                x1, y1, x2, y2 = map(int, det['bbox'])
                conf = det['confidence']
                label = det.get('label', 'fire').lower()
                
                # Dynamic Colors: Orange for Smoke, Red for Fire/Flame
                if 'smoke' in label:
                    color = (0, 165, 255) # BGR for Orange
                else:
                    color = (0, 0, 255)   # BGR for Red
                
                # Draw Box
                cv2.rectangle(processed_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw Label Background for better readability
                label_text = f"{label.upper()} {conf:.2f}"
                cv2.putText(processed_frame, label_text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            cv2.imshow("Intelligent Fire Detection System", processed_frame)
            ui.update() 
            
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    except Exception as e:
        print(f"System Error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        try:
            ui.root.destroy()
        except:
            pass

if __name__ == "__main__":
    main()