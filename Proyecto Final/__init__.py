import json
import colorama
from colorama import Fore, Style

from models.image import Image
from queries import select_input_image, get_similar_images
from load_data import load_images_from_folder

with open("config.json") as config_file:
    config = json.load(config_file)

folder_path = config["folder_path"]
query_image_path = config["query_image_path"]
quantity_images = config["quantity_images"]

if __name__ == "__main__":
    while True:
        print("#############################################")
        print("#                                           #")
        print("#" + Fore.GREEN + "     Bienvenido a Animals App GADD!        " + Style.RESET_ALL +"#")
        print("#                                           #")
        print("#############################################")
        print()
        print(Fore.BLUE + "### Seleccionar opcion ###" + Style.RESET_ALL )
        print(Fore.BLUE + "1." + Style.RESET_ALL + "Hacer una consulta")
        print(Fore.BLUE + "2." + Style.RESET_ALL + "Cargar datos")
        print(Fore.RED + "3." + Style.RESET_ALL + "Salir")

        option = input("Seleccionar una opcion (1/2/3): ")

        if option == "1":
            image_selected = select_input_image(query_image_path)
            get_similar_images(quantity_images, image_selected)
            input(Fore.BLUE +"Presione enter para continuar..." + Style.RESET_ALL)
        elif option == "2":
            load_images_from_folder(folder_path) 
            input(Fore.BLUE +"Presione enter para continuar..." + Style.RESET_ALL)
        elif option == "3":
            print("Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opcion invalida. Por favor seleccione una opcion valida." + Style.RESET_ALL)



    