from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, 'html.parser')

nameList = bs.span
for name in nameList:
    print(name.get_text())

print(" ")

print([tag for tag in bs.find_all('span', {'class':'green'})])
