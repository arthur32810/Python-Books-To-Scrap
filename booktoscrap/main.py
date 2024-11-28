from booktoscrap.soup import get_soup
from booktoscrap.constant import BASE_URL, STRING_TO_NUMBER
from booktoscrap.download import get_image, create_folder_category, create_data_folder
import csv


def get_text_in_array_information(soup, search_text):
    """Récupére un élément de la page dans le tableau information
    en fonction d'un texte de recherche"""
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

    product_description = soup.select_one("#product_description + p")
    information_book["product_description"] = (
        product_description.string if product_description else ""
    )

    information_book["category"] = soup.select("ul.breadcrumb li")[2].text.strip()

    information_book["review_rating"] = STRING_TO_NUMBER[
        soup.select_one(".star-rating").get("class")[1]
    ]

    information_book["image_url"] = BASE_URL + soup.select_one(
        ".carousel-inner div img"
    ).get("src").replace("../../", "")

    return information_book


# Avec yield
def get_books_link_in_page(url_page):
    """recupere tout les liens d'une page"""
    soup_category = get_soup(url_page)

    for link_book in soup_category.select(".product_pod h3 a"):
        yield BASE_URL + "catalogue/" + link_book.get("href").replace("../", "")


def get_category_pages(url_page_category):
    """récupérer les différentes lien des pages categories"""
    soup_page = get_soup(url_page_category)
    text_pagination = soup_page.select_one(".pager .current")

    if not text_pagination:
        return [url_page_category]

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
    links_categories.pop(0)

    for link_category in links_categories:
        category_url = BASE_URL + link_category.get("href")
        category_name = link_category.text.strip()

        yield category_url, category_name


def main():

    create_data_folder()

    for url_category, category_name in get_categories_link(BASE_URL):
        create_folder_category(category_name)

        # permet de définir les entetes lors de la premiere iteration
        first_iteration_book = True

        with open(f"./data/{category_name}/{category_name}.csv", "w") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")

            for url_category_page in get_category_pages(url_category):

                for url_book_page in get_books_link_in_page(url_category_page):

                    information_book = get_info_book(url_book_page)

                    get_image(
                        information_book["image_url"],
                        information_book["universal_product_code"],
                        f"./data/{category_name}",
                    )

                    if first_iteration_book:
                        writer.writerow(information_book.keys())
                        first_iteration_book = False

                    writer.writerow(information_book.values())
