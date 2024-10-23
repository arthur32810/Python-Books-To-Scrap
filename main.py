import requests
from bs4 import BeautifulSoup

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
    information_page={}
    information_page['universal_product_code'] = get_text_in_array_information(soup, 'UPC')
    information_page['title']=soup.select_one('.product_main h1').string.strip()
    information_page['price_including_tax'] = get_text_in_array_information(soup, 'Price (incl. tax)')
    information_page['price_excluding_tax'] = get_text_in_array_information(soup, 'Price (excl. tax)')
    
    #Garde uniquement les chiffres de la chaîne de caractére et les rassemble
    information_page['number_avaible']=''.join(filter(str.isdigit, get_text_in_array_information(soup, 'Availability')))
    
    information_page['product_description']= soup.select_one('#product_description + p').string
    information_page['category']=soup.select('ul.breadcrumb li')[2].text.strip()
    information_page['review_rating']=convert_string_in_number(soup.select_one('.star-rating').get('class')[1])
    information_page['image_url']=base_url + soup.select_one('.carousel-inner div img').get('src').replace('../../', '')
    
    return information_page

    
    
    
    
soup = get_soup(url)
get_info_page_with_soup(soup)