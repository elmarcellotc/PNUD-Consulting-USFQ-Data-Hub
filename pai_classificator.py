# USFQ Data Hub
# Marcello Coletti 00213379

#
# Author: Marcello Coletti; USFQ Data Hub
#
# Contact: coletti.marcello@gmail.com; +593939076444 (Ecuador)
#


# Description: This code is dessign to get the text of the Sustainable Development Goals. The search is in spanish
# because this code is part of the consulting programm to measure the SDG of the Republic of Ecuador.

# Required libraries:
import requests # To download the html
from bs4 import BeautifulSoup

# # This is the required function to get the soup (or an object of the web page searched).

def get_soup(url, get_content=True, url_type='html.parser'):
    
    # BeautifulSoup parses the content of the html document. This proccess is repeated along all this
    # script.
    
    if get_content == True:
        page = requests.get(url).content
    else:
        page = requests.get(url).text

    soup = BeautifulSoup(page, url_type)

    return soup

url = 'https://www.un.org/sustainabledevelopment/es/poverty/'

soup = get_soup(url)

for obj in soup.find_all("p"):
    
    print(obj.text)