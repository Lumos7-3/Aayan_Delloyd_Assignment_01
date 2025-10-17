import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import tkinter as tk

# Mediapipe face detection (bounding boxes)
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5
)

# Mediapipe face mesh (nose & eyes)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Webcam
cap = cv2.VideoCapture(0)

# Tkinter setup
root = tk.Tk()
root.title("Real-time Face Tracking")
root.geometry("960x720")
root.configure(bg="#0b0b0b")

# --- HEADER ---
header = tk.Frame(root, bg="#111111", height=60)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🎯 Real-time Face Tracking",
    font=("Helvetica Neue", 20, "bold"),
    fg="#00ff99",
    bg="#111111",
)
title.pack(side="left", padx=20, pady=10)

# --- MAIN VIDEO AREA ---
video_frame = tk.Frame(root, bg="#0b0b0b", padx=15, pady=15)
video_frame.pack(expand=True, fill="both")

lbl = tk.Label(video_frame, bg="#1a1a1a", bd=0, relief="flat")
lbl.pack(expand=True, fill="both")

# --- FOOTER ---
footer = tk.Frame(root, bg="#111111", height=70)
footer.pack(fill="x", side="bottom")

# Add subtle dividing line
separator = tk.Frame(root, bg="#222222", height=2)
separator.pack(fill="x", side="bottom")

running = True
latest_frame = None


def show_frame():
    global running, latest_frame
    if not running:
        return

    ret, frame_cv = cap.read()
    if not ret:
        root.after(10, show_frame)
        return

    # 🔁 Mirror the frame horizontally
    frame_cv = cv2.flip(frame_cv, 1)

    rgb = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB)
    results_mesh = face_mesh.process(rgb)
    results_det = face_detection.process(rgb)

    # Draw bounding boxes
    if results_det.detections:
        for idx, detection in enumerate(results_det.detections):
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame_cv.shape
            x1 = int(bboxC.xmin * w)
            y1 = int(bboxC.ymin * h)
            x2 = x1 + int(bboxC.width * w)
            y2 = y1 + int(bboxC.height * h)
            cv2.rectangle(frame_cv, (x1, y1), (x2, y2), (0, 255, 128), 2)
            cv2.putText(frame_cv, f'Face-{idx+1}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 128), 2)

    # Draw nose tip & eye centers
    if results_mesh.multi_face_landmarks:
        h, w, _ = frame_cv.shape
        for face_landmarks in results_mesh.multi_face_landmarks:
            # Nose tip
            nose = face_landmarks.landmark[1]
            nose_pt = (int(nose.x * w), int(nose.y * h))
            cv2.circle(frame_cv, nose_pt, 6, (255, 50, 50), -1)

            # Left eye
            left_indices = [33, 133, 159, 145, 153, 154]
            x_left = sum([face_landmarks.landmark[i].x for i in left_indices]) / len(left_indices)
            y_left = sum([face_landmarks.landmark[i].y for i in left_indices]) / len(left_indices)
            left_pt = (int(x_left * w), int(y_left * h))
            cv2.circle(frame_cv, left_pt, 6, (255, 50, 50), -1)

            # Right eye
            right_indices = [263, 362, 386, 374, 380, 385]
            x_right = sum([face_landmarks.landmark[i].x for i in right_indices]) / len(right_indices)
            y_right = sum([face_landmarks.landmark[i].y for i in right_indices]) / len(right_indices)
            right_pt = (int(x_right * w), int(y_right * h))
            cv2.circle(frame_cv, right_pt, 6, (255, 50, 50), -1)

    latest_frame = frame_cv.copy()

    # Convert for Tkinter
    frame_rgb = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    lbl.config(image=imgtk)
    lbl.image = imgtk

    root.after(10, show_frame)


def toggle_webcam():
    global running
    running = not running
    if running:
        show_frame()


def save_snapshot():
    global latest_frame
    if latest_frame is not None:
        filename = "snapshot.jpg"
        cv2.imwrite(filename, latest_frame)
        print(f"✅ Snapshot saved as {filename}")


def quit_app():
    cap.release()
    root.destroy()


# --- STYLED BUTTONS ---
def make_button(parent, text, cmd, color):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        activebackground="#2c2c2c",
        font=("Helvetica Neue", 11, "bold"),
        padx=14,
        pady=6,
        bd=0,
        relief="flat",
        highlightthickness=0,
        cursor="hand2"
    )


btn_start = make_button(footer, "▶ Start / Pause", toggle_webcam, "#00b894")
btn_snap = make_button(footer, "📸 Snapshot", save_snapshot, "#f39c12")
btn_quit = make_button(footer, "❌ Quit", quit_app, "#e74c3c")

btn_start.pack(side="left", padx=30, pady=15)
btn_snap.pack(side="left", padx=30, pady=15)
btn_quit.pack(side="left", padx=30, pady=15)

# Start loop
show_frame()
root.mainloop()
cap.release()

