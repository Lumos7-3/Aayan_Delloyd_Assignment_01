import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

# --- Load YOLO model ---
MODEL_PATH = "path/to/your/best.pt"


if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
    print("✅ Loaded trained YOLO model.")
else:
    print("⚠️ best.pt not found — using default YOLO model.")
    model = YOLO()

# --- Class names (match your data.yaml) ---
classes = ['license-plate', 'broken', 'non broken']

# --- Prediction ---
def predict_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return None

    results = model.predict(source=image_path, imgsz=640, conf=0.25, verbose=False)
    output = results[0]

    for box, conf, cls in zip(output.boxes.xyxy, output.boxes.conf, output.boxes.cls):
        x1, y1, x2, y2 = map(int, box)
        class_id = int(cls)

        if class_id >= len(classes):
            continue
        class_name = classes[class_id]

        # Skip drawing plain license plate if you only want broken/not broken
        if class_name == "license-plate":
            continue

        confidence_pct = int(conf * 100)
        label = f"{class_name} ({confidence_pct}%)"

        color = (0, 0, 255) if class_name == "broken" else (0, 255, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# --- GUI Functions ---
def show_image(image_path):
    image = predict_image(image_path)
    if image is None:
        messagebox.showerror("Error", "Could not process the image.")
        return

    image_pil = Image.fromarray(image)
    image_pil = image_pil.resize((600, 400), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image_pil)
    panel.config(image=image_tk)
    panel.image = image_tk

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if file_path:
        show_image(file_path)

# --- Tkinter Window Styling ---
root = tk.Tk()
root.title("License Plate Damage Detection")
root.geometry("800x600")
root.configure(bg="black")

panel = tk.Label(root, bg="black")
panel.pack(padx=10, pady=10)

btn_image = tk.Button(root,
                      text="Upload Image",
                      command=upload_image,
                      bg="red",
                      fg="white",
                      activebackground="darkred",
                      font=("Helvetica", 12, "bold"),
                      relief="flat",
                      padx=15, pady=10)
btn_image.pack(pady=20)

title_label = tk.Label(root,
                       text="LICENSE PLATE DAMAGE DETECTION",
                       bg="black",
                       fg="red",
                       font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

root.mainloop()
