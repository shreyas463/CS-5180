from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page1.html')

bs = BeautifulSoup(html, 'html.parser')

#printing only h1 content
print(bs.h1)
print(bs.html.body.h1)
print(bs.body.h1)
print(bs.html.h1)