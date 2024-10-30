import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
BASE_URL = "https://books.toscrape.com/"

STRING_TO_NUMBER = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url):
    # Récupération d'un seul livre
    response = requests.get(url)
    # Forcer l'encodage correct (UTF-8)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def get_text_in_array_information(soup, search_text):
    # Récupére un élément de la page dans le tableau information
    # en fonction d'un texte de recherche
    return soup.find("th", string=search_text).find_next_sibling("td").string.strip()


def get_info_book(url_book):
    soup = get_soup(url_book)

    # Récupération des informations nécéssaire dans un dictionnaire
    information_book = {}

    information_book["universal_product_code"] = get_text_in_array_information(
        soup, "UPC"
    )

    information_book["title"] = soup.select_one(".product_main h1").string.strip()

    information_book["price_including_tax"] = get_text_in_array_information(
        soup, "Price (incl. tax)"
    )
    information_book["price_excluding_tax"] = get_text_in_array_information(
        soup, "Price (excl. tax)"
    )

    # Garde uniquement les chiffres de la chaîne de caractére et les rassemble
    information_book["number_avaible"] = "".join(
        filter(str.isdigit, get_text_in_array_information(soup, "Availability"))
    )

    information_book["product_description"] = soup.select_one(
        "#product_description + p"
    ).string

    information_book["category"] = soup.select("ul.breadcrumb li")[2].text.strip()

    information_book["review_rating"] = STRING_TO_NUMBER[
        soup.select_one(".star-rating").get("class")[1]
    ]

    information_book["image_url"] = BASE_URL + soup.select_one(
        ".carousel-inner div img"
    ).get("src").replace("../../", "")

    return information_book


def get_books_link_in_page(url_page):

    # recupere tout les liens d'une page
    soup_category = get_soup(url_page)
    array_url_book = []

    for link_book in soup_category.select(".product_pod h3 a"):
        array_url_book.append(
            BASE_URL + "catalogue/" + link_book.get("href").replace("../", "")
        )

    return array_url_book


def get_category_pages(url_page_category):
    # récupérer les différentes lien des pages categories
    soup_page = get_soup(url_page_category)
    text_pagination = soup_page.select_one(".pager .current")

    if not text_pagination:
        return url_page_category

    number_of_page = int(text_pagination.text.split("of ")[-1].strip()) + 1
    array_link_page = [url_page_category]

    for number_page in range(2, number_of_page):
        array_link_page.append(
            url_page_category.replace("index.html", f"page-{number_page}.html")
        )

    return array_link_page


def get_categories_link(base_url):
    soup_page = get_soup(base_url)
    links_categories = soup_page.select(".nav-list a")
    array_url_categories = []

    for link_category in links_categories:
        array_url_categories.append(BASE_URL + link_category.get("href"))

    return array_url_categories


def main():

    # permet de définir les entetes lors de la premiere iteration
    first_iteration_book = True
    with open("data.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        for url_category in get_categories_link(BASE_URL):
            for url_category_page in get_category_pages(url_category):
                for url_book_page in get_books_link_in_page(url_category_page):
                    information_book = get_info_book(url_book_page)
                    if first_iteration_book:
                        writer.writerow(information_book.keys())
                        first_iteration_book = False

                    writer.writerow(information_book.values())


if __name__ == "__main__":
    # main()
    print(get_categories_link(BASE_URL))
