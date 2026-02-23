import onnxruntime as ort
import numpy as np
from PIL import Image
import os
from django.conf import settings

# ================= MODEL PATH =================
MODEL_PATH = os.path.join(settings.BASE_DIR, "plant_model.onnx")

# ================= LOAD MODEL =================
session = ort.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name

# ================= DISEASE CLASS NAMES =================
# ⚠️ CHANGE THESE based on your training dataset
# Example PlantVillage dataset (edit if needed)

class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn___Common_rust",
    "Corn___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight"
]

# ================= PREDICTION FUNCTION =================
def predict_image(img_path):
    # open image
    img = Image.open(img_path).convert("RGB")

    # resize (must match training size)
    img = img.resize((128, 128))

    # normalize
    img = np.array(img).astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # run model
    outputs = session.run(None, {input_name: img})
    prediction_index = np.argmax(outputs[0])

    # safety check
    if prediction_index >= len(class_names):
        return f"Unknown disease (Class {prediction_index})"

    return class_names[prediction_index]