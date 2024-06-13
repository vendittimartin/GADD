from load_data import load_images_from_folder
import cv2
from models.image import Image
from colorama import Fore, Style
from load_data import load_query_images_from_folder
from model import extract_features
from database.db_cursor import get_similar_images

def select_input_image(query_image_path):
    while True:
        image_names = load_query_images_from_folder(query_image_path)

        print("Seleccionar la imagen a utilizar:")
        for i, image_name in enumerate(image_names, 1):
            print(f"{i}. Imagen: {image_name}")

        selected_index = int(input("Selecciona una imagen (1 a {}): ".format(len(image_names)))) - 1

        if 0 <= selected_index < len(image_names):
            selected_image = image_names[selected_index]
            features = extract_features(query_image_path)
            image = Image(features, selected_image)
            print(Fore.GREEN + "Imagen seleccionada:" + selected_image + Style.RESET_ALL)
            return image
        else:
            print(Fore.RED + "Selección inválida." + Style.RESET_ALL)


def get_similar_images(quantity_images, image_selected):
    print(image_selected)
    #get_similar_images(quantity_images, image_selected)