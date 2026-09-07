# Teknofest UAV Area Detection

Computer vision experiments for detecting a colored target (a red bottle) in
a camera feed and reporting which zone of a 3x3 grid it is in, built for a
high-school UAV competition.

> TODO: add the course/resource that inspired this project

## Features

- HSV color-range masking with live trackbar tuning for red-object detection
- Contour-based shape classification (triangle, rectangle, circle)
- 3x3 zone grid (Top-Left, Top, Top-Right, Left, Center, Right,
  Bottom-Left, Bottom, Bottom-Right) to report where a detected rectangle is
  positioned in the frame
- Multi-color (red/green/blue) detection with bounding boxes
- Streaming frames from a phone's IP Webcam app as an alternative video source

## Tech stack

- Python 3
- OpenCV (`opencv-python`)
- NumPy
- Requests (for the phone camera stream)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Each script opens the default webcam (`cv2.VideoCapture(0)`) unless noted
otherwise, and can be closed with the `Esc` or `q` key depending on the
script.

```bash
# Detect a rectangular colored target and report its zone in the frame
python src/area_detection.py

# Detect red, green and blue regions with bounding boxes
python src/color_detection.py

# Minimal camera loop used for the drone's onboard target search
python src/bottle_area_detection.py

# Stream frames from a phone running the IP Webcam app instead of a webcam
python src/phone_camera_stream.py
```

`src/area_detection.py` and `src/color_detection.py` open an extra
"Trackbars" / control window — use the sliders to tune the HSV thresholds
for your lighting conditions and target color.

`experiments/` contains earlier draft versions of the scripts above, kept
for reference rather than active use.

`data/colors.csv` is the public-domain color name dataset from
[codebrainz/color-names](https://github.com/codebrainz/color-names), used as
a reference table for color detection experiments.

## Project structure

```
src/            Main detection scripts
experiments/    Earlier draft versions, kept for reference
data/           Reference data (color name table)
```

## Limitations

- HSV thresholds are tuned for a specific red object and lighting setup;
  they will need re-tuning for other targets or environments
- No unit tests
- `src/bottle_area_detection.py` only opens the camera feed — the actual
  color-detection logic for it is still commented out
- Zone detection assumes a fixed 640x480 frame size

This project was a simple self-study exercise I built in high school (2021)
to develop my computer/programming skills through courses I was taking at
the time. It was reorganized and cleaned up in 2026 for public release.

## License

MIT
