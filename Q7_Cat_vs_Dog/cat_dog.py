import torch
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os

# --- Load pre-trained model ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()
model.to(device)

# Cat/Dog determination based on ImageNet indices
def is_cat_or_dog(idx):
    if 151 <= idx <= 268:
        return "Dog"
    elif 281 <= idx <= 285:
        return "Cat"
    else:
        return "Other"

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- GUI Setup ---
root = tk.Tk()
root.title("🐾 Cat vs Dog Classifier")
root.geometry("900x700")
root.configure(bg="#1c1c2b")

# --- Image Display Frame ---
img_frame = tk.Frame(root, bg="#2c2c3a", bd=3, relief="ridge")
img_frame.pack(pady=20, padx=20, fill="both", expand=True)

img_label = tk.Label(img_frame, bg="#2c2c3a")
img_label.pack(pady=10, expand=True)

# --- Result Display ---
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Helvetica", 18, "bold"),
                        fg="#00ffcc", bg="#1c1c2b")
result_label.pack(pady=10)

# --- Functions ---
def choose_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if path:
        img = Image.open(path).convert("RGB")
        img.thumbnail((500, 500))
        imgtk = ImageTk.PhotoImage(img)
        img_label.imgtk = imgtk
        img_label.config(image=imgtk)
        classify_image(img)

def classify_image(pil_img):
    # Preprocess
    input_tensor = preprocess(pil_img).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)[0]
        conf, idx = torch.max(probabilities, 0)
        idx = idx.item()
        conf = conf.item() * 100  # Convert to %
        label = is_cat_or_dog(idx)
    
    result_text.set(f"Prediction: {label} ({conf:.2f}%)")

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#1c1c2b")
btn_frame.pack(pady=10)

button_style = {"font": ("Helvetica", 13, "bold"), "bd":0, "relief":"ridge", "width":20, "height":2}

tk.Button(btn_frame, text="📂 Choose Image", bg="#00b894", fg="white",
          **button_style, command=choose_image).grid(row=0, column=0, padx=20)

tk.Button(btn_frame, text="❌ Quit", bg="#d63031", fg="white",
          **button_style, command=root.destroy).grid(row=0, column=1, padx=20)

root.mainloop()
