from bs4 import BeautifulSoup

bs = BeautifulSoup("<HTML><body><h1>Trash</h1><h1>Title</h1></body><HTML>", 'html.parser')
print(bs.h1)

