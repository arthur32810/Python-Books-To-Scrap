def get_image(url_image, upc_book, destination_path):
    """Téléchargement de l'image du livre"""
    import requests

    response = requests.get(url_image)
    extension = url_image.split(".")[-1]

    with open(f"{destination_path}/{upc_book}.{extension}", "wb") as file:
        file.write(response.content)


def create_folder_category(name_category):
    """Création d'un dossier par catégory grace au paquet os"""
    import os

    destination_path = "./data/" + name_category
    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
