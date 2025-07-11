# AzrielProject

This repository contains a minimal prototype for streaming video from a Jetson Nano based drone and viewing it over the web. The backend is a small Flask server that provides a single endpoint for a MJPEG stream. The frontend is a lightweight React page. YOLO is used for basic computer vision so the frames can be annotated in real time.

You can run everything on the Jetson or on a regular laptop to experiment. As long as the machine has `opencv-python` and a camera, the code will stream video.

## Structure

- `server/` – Flask backend that captures video, runs YOLO and streams the video frames.
- `client/` – simple React page served by Flask. It fetches the video stream.

## Requirements

On the Jetson Nano install these Python packages:

```bash
pip install -r server/requirements.txt
```

The YOLO model uses the `ultralytics` package which can be heavy. Ensure you have the required dependencies installed on the Jetson (CUDA, etc.).

## Running

1. Start the Flask server on the Jetson or any machine with a camera. The server binds to `0.0.0.0` so it can be reached from other devices on the same network:

```bash
python3 server/app.py
```

2. Determine the IP address of the device running the server. On your laptop or phone open `http://<jetson-ip>:5000` to view the stream. Replace `5000` if you set a different port.

3. (Optional) Expose the server publicly using `ngrok` so it can be accessed outside your local network:

```bash
ngrok http 5000
```

Use the forwarding URL printed by ngrok in any browser.

## Notes

- The example uses the default camera at `/dev/video0`. Adjust `VideoCapture` if your camera uses another index or pipeline.
- The YOLO detection overlay is basic but demonstrates how to integrate AI vision.

## Next Steps

- Configure authentication if you expose the stream publicly.
- Experiment with different YOLO models for improved accuracy or speed.
- Add flight controls or telemetry endpoints to the Flask server.
