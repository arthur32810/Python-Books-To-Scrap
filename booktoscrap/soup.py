import requests
from bs4 import BeautifulSoup


def get_soup(url):
    # Récupération d'un seul livre
    response = requests.get(url)
    # Forcer l'encodage correct (UTF-8)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")