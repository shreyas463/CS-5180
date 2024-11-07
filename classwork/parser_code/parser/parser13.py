from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

gifts = bs.find(id='giftList').find_all('tr',{'class':'gift'})
print(len(gifts))




