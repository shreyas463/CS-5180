from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(), 'html.parser')

tagList = bs.find_all('span', {'class':['green', 'red']})

for tag in tagList:
    print(tag.get_text())