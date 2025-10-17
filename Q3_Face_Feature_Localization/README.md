# Real-time Face Tracking (OpenCV + Mediapipe + Tkinter)

This program uses **OpenCV** and **Mediapipe** to detect faces, track facial landmarks (nose & eyes), and display the video stream in a simple **Tkinter GUI**.  
You can also **take snapshots** of the live video.

---

## 📂 Files
- `detect_faces.py` → Main program
- `shape_predictor_68_face_landmarks.dat` → (Not directly used, but kept in the folder if needed later)

---

## ⚙️ Installation
1. Clone this project or download the files.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

	
## ALSO VERY IMPORTANT

Before running the script be sure to download shape_predictor_68_face_landmarks.dat.bz2 and unzip the file and save it in this folder. Only then will it work

## Run the script

python detect_faces.py
