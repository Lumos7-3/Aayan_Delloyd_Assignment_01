import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

# --- Mediapipe for robust multi-face tracking ---
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# --- GUI Setup ---
root = tk.Tk()
root.title("🔥 Real-time Multi-Face Blur (Mirrored)")
root.geometry("900x700")
root.configure(bg="#1e1e2f")

# Video label
video_lbl = tk.Label(root, bg="black")
video_lbl.pack(pady=10, expand=True)

# Global variables
cap = cv2.VideoCapture(0)
blur_strength = tk.DoubleVar(value=0.8)
running = True
latest_frame = None

# --- Functions ---
def apply_face_blur(frame, faces, strength=0.8):
    for face in faces:
        # face bbox in pixels
        x1 = max(int(face.location_data.relative_bounding_box.xmin * frame.shape[1]), 0)
        y1 = max(int(face.location_data.relative_bounding_box.ymin * frame.shape[0]), 0)
        w = int(face.location_data.relative_bounding_box.width * frame.shape[1])
        h = int(face.location_data.relative_bounding_box.height * frame.shape[0])
        x2, y2 = x1 + w, y1 + h
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            continue
        # stronger blur for moving faces
        kW = max(1, int((w // 2) * strength) | 1)
        kH = max(1, int((h // 2) * strength) | 1)
        frame[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (kW, kH), 0)
    return frame

def update_frame():
    global latest_frame
    if not running:
        return
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    # 🔁 Mirror the frame horizontally
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb)
    if results.detections:
        frame = apply_face_blur(frame, results.detections, blur_strength.get())
    latest_frame = frame.copy()

    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    video_lbl.imgtk = imgtk
    video_lbl.config(image=imgtk)
    root.after(10, update_frame)

def stop_webcam():
    global running
    running = False
    cap.release()
    root.destroy()

def snapshot():
    if latest_frame is not None:
        cv2.imwrite("snapshot.jpg", latest_frame)
        print("✅ Snapshot saved as snapshot.jpg")

# --- GUI Controls ---
ctrl_frame = tk.Frame(root, bg="#1e1e2f")
ctrl_frame.pack(pady=10)

tk.Button(ctrl_frame, text="📸 Snapshot", bg="#ff6f61", fg="white", font=("Arial",12,"bold"),
          command=snapshot).grid(row=0, column=0, padx=8)
tk.Button(ctrl_frame, text="❌ Quit", bg="#c0392b", fg="white", font=("Arial",12,"bold"),
          command=stop_webcam).grid(row=0, column=1, padx=8)

tk.Label(ctrl_frame, text="Blur Strength:", bg="#1e1e2f", fg="white", font=("Arial",12,"bold")).grid(row=0,column=2,padx=5)
tk.Scale(ctrl_frame, variable=blur_strength, from_=0.1, to=1.5, resolution=0.05, orient="horizontal",
         length=200, bg="#1e1e2f", fg="white", troughcolor="#555555").grid(row=0,column=3,padx=5)

# Start webcam
update_frame()
root.mainloop()
