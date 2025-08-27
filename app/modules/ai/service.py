import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess

# Load pre-trained model
# MODEL_PATH = "app/model_weights.keras"
MODEL_PATH = "app/NewModel.keras"
# MODEL_PATH = 'https://drive.google.com/file/d/1cKFH7_TGwH-lJqB6K9iEMlvdGGnm_f4A/view?usp=sharing'
InceptionV3_model = load_model(MODEL_PATH)

# MAMO_CHECK_MODEL_PATH = "app/mamoClassifier.keras"
# mamo_check_model = load_model(MAMO_CHECK_MODEL_PATH)

# def load_and_preprocess_image(img_path, target_size=(299, 299), rescale=1.0 / 255):
#     img = image.load_img(img_path, target_size=target_size)
#     img_array = image.img_to_array(img)

#     # Apply rescaling
#     img_array *= rescale

#     # Expand dimensions for model prediction
#     img_array = np.expand_dims(img_array, axis=0)

#     return img_array

def load_and_preprocess_image(img_path, target_size=(260, 260), rescale=1.0 / 255):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)

    # Apply rescaling
    img_array *= rescale

    # Expand dimensions for model prediction
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def load_and_preprocess_image(img_path, target_size=(260, 260)):
    # Load and resize image
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)

    # Preprocess using EfficientNet's preprocessing
    img_array = efficientnet_preprocess(img_array)

    # Expand dimensions to make it batch-like
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

# def isMamoImage(processed_img):
#     img_prediction = mamo_check_model.predict(processed_img)
#     print('first img_prediction', img_prediction)

#     # Threshold-based classification
#     threshold = 0.5
#     img_class = np.where(img_prediction > threshold, 1, 0)
#     print('first img_class', img_class)

#     return False if img_class[0][0] == 1 else True

def predict_image(img_path):
    processed_img = load_and_preprocess_image(img_path)
    # isMamo = isMamoImage(processed_img)
    # if not isMamo:
    #     return "notMamo"
    # else:        
    #     img_prediction = InceptionV3_model.predict(processed_img)
    img_prediction = InceptionV3_model.predict(processed_img)
    print('first', img_prediction)

    # Threshold-based classification
    threshold = 0.5
    img_class = np.where(img_prediction > threshold, 1, 0)
    certainty = np.maximum(img_prediction, 1 - img_prediction) * 100
    certainty_str = f"{certainty[0][0]:.2f}%"
    return f"malignant-{certainty_str}"  if img_class[0][0] == 1 else f"benign-{certainty_str}"
