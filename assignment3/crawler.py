from urllib.request import urlopen
from bs4 import BeautifulSoup
# html = urlopen('https://neetcode.io/practice')
html = urlopen('http://www.pythonscraping.com/pages/page1.html')
# bs = BeautifulSoup(html.read(), 'html.parser')
# print(bs.h1)
# bs = BeautifulSoup("<HTML><body><p>Some text</p></body><HTML>", 'html.parser')
# print(bs.body.prettify())
# bs = BeautifulSoup(html.read(), 'html.parser')  # entire parse tree

bs = BeautifulSoup(html.read(), 'lxml')
bs.find_all('div', class_='content', limit=3)


print(bs)
