import requests
from bs4 import BeautifulSoup

#Récupération d'un seul livre
url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

page= requests.get(url).content
soup = BeautifulSoup(page, 'html.parser')
print(soup.title.string)