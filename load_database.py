import os
import psycopg2
import json
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np

# Cargar configuración de conexión desde config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Configuración de la conexión a PostgreSQL
conn = psycopg2.connect(
    dbname=config['dbname'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port']
)
cursor = conn.cursor()

# Cargar el modelo ResNet-18 preentrenado
modelo_resnet = models.resnet18(pretrained=True)
modelo_resnet.eval()

# Transformaciones de imagen para el modelo ResNet
transformacion = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image_path):
    image = Image.open(image_path)
    image_tensor = transformacion(image).unsqueeze(0)  # Agregar dimensión de lote (batch)

    with torch.no_grad():
        caracteristicas = modelo_resnet(image_tensor)

    caracteristicas_vector = caracteristicas.squeeze().numpy()
    return caracteristicas_vector

# Directorio de imágenes
image_dir = config['path']
for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)
    features = extract_features(image_path)

    # Insertar características en la base de datos
    cursor.execute(
        "INSERT INTO imagenes (url, caracteristicas) VALUES (%s, %s)",
        (image_name, features.tolist())
    )

conn.commit()
cursor.close()
conn.close()
