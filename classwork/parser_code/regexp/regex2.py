from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

regexp = re.compile(r'\$(\d+,)?\d+\.\d+\n')
prices = bs.find_all(string=regexp)
for price in prices:
    print(price.strip())

print()

x = re.search("^The.*Spain$", "The rain in Spain")
print(x.string)
