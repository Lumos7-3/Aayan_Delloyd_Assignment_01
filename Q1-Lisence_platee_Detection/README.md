# License Plate Character Break Detection

## Project Overview
This project detects **broken or damaged characters** on vehicle license plates from **front (FR)** and **rear (RE)** images or videos. It uses a **YOLO-based deep learning model** trained on labeled datasets sourced from **Roboflow**.  

The system includes:  
- A **training notebook** to preprocess data and train the model.  
- A **GUI Python script** to perform real-time detection on images or videos.  

---

## File Structure
```
├── train_model.ipynb           # Notebook to load, preprocess, and train the model
├── detect_plate_damage.py      # GUI script for image/video inference
├── dataset/                    # Folder containing Roboflow dataset (FR & RE images)
├── runs/detect/train/weights/  # Folder to save trained YOLO weights
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and instructions
```

---

## Dependencies
Install required packages with:

```bash
pip install -r requirements.txt
```

Common packages:
- `torch` / `torchvision`  
- `ultralytics` (YOLO)  
- `opencv-python`  
- `Pillow`  
- `numpy`  
- `tkinter` (usually pre-installed with Python)  

---

## Training the Model

1. Open `train_model.ipynb` in **Jupyter Notebook** or **Google Colab**.
2. Load your dataset from Roboflow by updating the dataset URL and API key.
3. Run the notebook to:
   - Preprocess and augment images  
   - Load a pre-trained YOLO model  
   - Train/fine-tune the model on your dataset  
   - Save the trained weights (e.g., `best.pt`) in `runs/detect/train/weights/`

> **Tip:** Ensure the dataset is properly labeled as `broken` and `non broken` for accurate detection.

---

## Running Inference (GUI)

1. Open `detect_plate_damage.py`.
2. Ensure the path to your trained model weights is correct:

```python
model = YOLO("runs/detect/train/weights/best.pt")
```

3. Run the script:

```bash
python detect_plate_damage.py
```

4. Use the GUI to:
   - **Upload Image:** Select an image to detect broken/non-broken license plate characters.  
   - **Upload Video:** Select a video to detect character damage frame by frame.  

5. Detection Results:
   - **Red bounding box:** `broken`  
   - **Green bounding box:** `non broken`  
   - Labels include class and confidence score.

> **Screenshot Example:**  
> *(Replace with an actual screenshot of your GUI)*  
> ![GUI Example](path_to_screenshot.png)

---

## Notes & Tips
- Ensure images/videos are clear and license plates are fully visible.  
- Adjust YOLO parameters (`imgsz`, `conf`) and training hyperparameters as needed.  
- The GUI resizes images to 600x400 px, but you can modify the code for different window sizes.  
- You can extend the project to other vehicle datasets or different plate types.  

---

## Example Workflow
1. Train your model using `train_model.ipynb`.  
2. Save trained weights as `best.pt`.  
3. Launch `detect_plate_damage.py` to test new images/videos.  

