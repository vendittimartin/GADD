from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import psycopg2
import numpy as np
import os
import json
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        uploaded_features = extract_features(file_path)

        if uploaded_features is None or np.isnan(uploaded_features).any():
            return render_template('index.html', error="La imagen subida contiene características no válidas (NaN).")

        cursor.execute(
                    """
                    SELECT url, cosine_distance(caracteristicas, %s::FLOAT8[]) AS distance
                    FROM imagenes
                    ORDER BY distance
                    LIMIT 200
                    """,
                    (uploaded_features.tolist(),)
                )
        
        similar_images = cursor.fetchall()

        unique_images = []
        seen_urls = set()

        for img in similar_images:
            url = img[0]
            if url not in seen_urls:
                unique_images.append(img)
                seen_urls.add(url)

            if len(unique_images) >= 100:
                break

        input_image_path = os.path.join(config['input_path'], filename)
        print(input_image_path)

        image_base_path = config['static_dataset']
        similar_images_full_path = [(os.path.join(image_base_path, img[0]), img[1]) for img in unique_images]
        print(similar_images_full_path)

        return render_template('results.html', input_image=input_image_path, similar_images=similar_images_full_path)
    return redirect(url_for('index'))

@app.route('/load_data', methods=['POST'])
def load_data():
    os.system('python load_database.py')
    return 'Datos cargados correctamente.', 200

def extract_features(image_path):
    image = Image.open(image_path)
    image_tensor = transformacion(image).unsqueeze(0)

    with torch.no_grad():
        caracteristicas = modelo_resnet(image_tensor)

    caracteristicas_vector = caracteristicas.squeeze().numpy()
    return caracteristicas_vector

if __name__ == '__main__':
    app.run(debug=True)
