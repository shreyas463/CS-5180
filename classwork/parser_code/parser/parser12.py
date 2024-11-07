from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.cpp.edu/')
bs = BeautifulSoup(html.read(), 'html.parser')

title = bs.find_all('div', {'id':'consent-box'})
print(title)



