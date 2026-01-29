import cv2
from pc_system.modules.video_input import get_video_stream, process_frame
from pc_system.modules.detection.py import FireDetector # Adjust path if needed

# Replace with a link to a fire video for testing
source = "https://www.youtube.com/watch?v=TEST_FIRE_VIDEO" 
stream_url = get_video_stream(source)
cap = cv2.VideoCapture(stream_url)
detector = FireDetector()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame = process_frame(frame)
    results = detector.detect(frame)
    
    # Simple display
    cv2.imshow("Fire Detection Prototype", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()