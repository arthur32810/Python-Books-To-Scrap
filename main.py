import requests
from bs4 import BeautifulSoup
import csv

url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
base_url="https://books.toscrape.com/"
 
def get_soup(url):
    #Récupération d'un seul livre
    response= requests.get(url)
    # Forcer l'encodage correct (UTF-8)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

def get_text_in_array_information(soup, search_text):
    #Récupére un élément de la page dans le tableau information en fonction d'un texte de recherche
    return soup.find('th', string=search_text).find_next_sibling('td').string.strip()

def convert_string_in_number(stringNumber):
    #Converti un nombre écrit en lette sous forme de chiffre
    string_to_number={
        'One':1,
        'Two':2,
        'Three':3,
        'Four':4,
        'Five':5
    }
    
    return string_to_number[stringNumber]    

def get_info_page_with_soup(soup):
    #Récupération des informations nécéssaire dans un dictionnaire
    information_book={}
    information_book['universal_product_code'] = get_text_in_array_information(soup, 'UPC')
    information_book['title']=soup.select_one('.product_main h1').string.strip()
    information_book['price_including_tax'] = get_text_in_array_information(soup, 'Price (incl. tax)')
    information_book['price_excluding_tax'] = get_text_in_array_information(soup, 'Price (excl. tax)')
    
    #Garde uniquement les chiffres de la chaîne de caractére et les rassemble
    information_book['number_avaible']=''.join(filter(str.isdigit, get_text_in_array_information(soup, 'Availability')))
    
    information_book['product_description']= soup.select_one('#product_description + p').string
    information_book['category']=soup.select('ul.breadcrumb li')[2].text.strip()
    information_book['review_rating']=convert_string_in_number(soup.select_one('.star-rating').get('class')[1])
    information_book['image_url']=base_url + soup.select_one('.carousel-inner div img').get('src').replace('../../', '')
    
    return information_book

def generate_csv_file(dictionnaire):
    
    
    with open('data.csv', 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(dictionnaire.keys())
        
        writer.writerow(dictionnaire.values())
    
    
def main():
    soup = get_soup(url)
    information_book = get_info_page_with_soup(soup)
    generate_csv_file(information_book)

if __name__ == "__main__":
    main()