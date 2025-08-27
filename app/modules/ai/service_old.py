import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Load pre-trained model
MODEL_PATH = "app/model_weights.keras"
InceptionV3_model = load_model(MODEL_PATH)

def load_and_preprocess_image(img_path, target_size=(299, 299), rescale=1.0 / 255):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)

    # Apply rescaling
    img_array *= rescale

    # Expand dimensions for model prediction
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

def predict_image(img_path):
    processed_img = load_and_preprocess_image(img_path)

    img_prediction = InceptionV3_model.predict(processed_img)
    print(img_prediction)

    # Threshold-based classification
    threshold = 0.5
    img_class = np.where(img_prediction > threshold, 1, 0)

    return "malignant" if img_class[0][0] == 1 else "benign"