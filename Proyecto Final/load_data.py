import os
from models.image import Image as ImageData
from model import extract_features
from sklearn.metrics.pairwise import cosine_similarity
from database.db_cursor import insert_image

def load_images_from_folder(folder):
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            features = extract_features(img_path)
            features_list = features.tolist()
            image = ImageData(features_list, filename)
            insert_data(image)

def load_query_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            images.append(filename)
    return images

def insert_data(image):
    insert_image(image)
            