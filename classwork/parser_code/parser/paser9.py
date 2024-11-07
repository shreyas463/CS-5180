from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html.read(), 'html.parser')

tagList = bs.find_all(['h1','h2','h3','h4','h5','h6'])

print(tagList)
for tag in tagList:
    print(tag.get_text())


