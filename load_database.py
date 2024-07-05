import os
import psycopg2
import json
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np

with open('config.json', 'r') as f:
    config = json.load(f)

conn = psycopg2.connect(
    dbname=config['dbname'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port']
)
cursor = conn.cursor()

modelo_resnet = models.resnet18(pretrained=True)
modelo_resnet.eval()

transformacion = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image_path):
    image = Image.open(image_path)
    image_tensor = transformacion(image).unsqueeze(0)

    with torch.no_grad():
        caracteristicas = modelo_resnet(image_tensor)

    caracteristicas_vector = caracteristicas.squeeze().numpy()
    return caracteristicas_vector

image_dir = config['static_dataset']
for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)
    features = extract_features(image_path)

    cursor.execute(
        "INSERT INTO imagenes (url, caracteristicas) VALUES (%s, %s)",
        (image_name, features.tolist())
    )

    print("imagen insertada correctamente" + image_name)

conn.commit()
cursor.close()
conn.close()
