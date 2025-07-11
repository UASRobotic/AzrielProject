import io
import threading
import time

from flask import Flask, Response, send_from_directory
import cv2

try:
    from ultralytics import YOLO
    yolo_model = YOLO('yolov8n.pt')
except Exception as e:
    yolo_model = None
    print(f"YOLO model could not be loaded: {e}")

app = Flask(__name__, static_folder='../client')

camera_lock = threading.Lock()
video_capture = cv2.VideoCapture(0)


def generate_frames():
    while True:
        with camera_lock:
            success, frame = video_capture.read()
        if not success:
            time.sleep(0.1)
            continue

        if yolo_model:
            # run inference
            results = yolo_model(frame)
            annotated_frame = results[0].plot()
        else:
            annotated_frame = frame

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return send_from_directory('../client', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
