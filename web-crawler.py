#downloadlinks
import requests
from bs4 import BeautifulSoup

page = requests.get('https://en.wikipedia.org/wiki/Roman_Empire')
bsoup = BeautifulSoup(page.content, 'html.parser')
links_list = bsoup.find_all('a')

for link in links_list:
    if 'href' in link.attrs:
        print(str(link.attrs['href']))