import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Load ResNet50 without top (classification) layers and specify input shape
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Create the final feature extraction model using a selected intermediate layer
intermediate_layer_name = 'conv5_block3_out'  # Example intermediate layer name from ResNet50
intermediate_layer_output = base_model.get_layer(intermediate_layer_name).output

# Create the feature extraction model
model = Model(inputs=base_model.input, outputs=intermediate_layer_output)

def load_and_preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def extract_features(image_path):
    img = load_and_preprocess_image(image_path)
    features = model.predict(img, verbose=False)
    return features.flatten()
