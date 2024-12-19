from flask import Flask, Response
from flask_cors import CORS
import cv2
from ultralytics import YOLO
from vidgear.gears import CamGear
import threading

app = Flask(__name__)
CORS(app)

# Load YOLO model
model = YOLO('yolov8n.pt')

# Video source (YouTube stream or local)
stream = CamGear(source="https://www.youtube.com/watch?v=3sgewysRGZY", stream_mode=True, logging=True).start()
threshold = 0.5

def generate_frames():
    while True:
        frame = stream.read()
        if frame is None:
            break

        results = model(frame)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            if score > threshold:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{model.names[int(class_id)]} {score:.2f}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
