import os

import numpy as np
from tensorflow.keras.applications.efficientnet import \
    preprocess_input as efficientnet_preprocess
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = "app/NewModel.keras"
InceptionV3_model = load_model(MODEL_PATH)

def load_and_preprocess_image(img_path, target_size=(260, 260), rescale=1.0 / 255):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)

    img_array *= rescale

    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def load_and_preprocess_image(img_path, target_size=(260, 260)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)

    img_array = efficientnet_preprocess(img_array)

    img_array = np.expand_dims(img_array, axis=0)

    return img_array

def predict_image(img_path):
    processed_img = load_and_preprocess_image(img_path)
    img_prediction = InceptionV3_model.predict(processed_img)
    print('first', img_prediction)

    threshold = 0.5
    img_class = np.where(img_prediction > threshold, 1, 0)
    certainty = np.maximum(img_prediction, 1 - img_prediction) * 100
    certainty_str = f"{certainty[0][0]:.2f}%"
    return f"malignant-{certainty_str}"  if img_class[0][0] == 1 else f"benign-{certainty_str}"
